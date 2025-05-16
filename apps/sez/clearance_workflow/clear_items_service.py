import logging
from typing import List, Dict, Any, Optional

from django.db import transaction

from apps.declaration.models import DeclaredItem
from apps.sez.clearance_workflow.vznab_stock_service import fetch_vznab_stock_flat_tree, PanelError
from apps.sez.models import ClearedItem

logger = logging.getLogger(__name__)


def fetch_stock_tree_with_row_numbers(
    order_id: int,
    root_scp_unv: int,
    count: float = 1.0,
    max_depth: Optional[int] = None,
    tv: bool = False,
) -> List[Dict[str, Any]]:
    """
    Build a flat list of all components for a given specification and enrich each item with
    its `row_number` and `nom_reg` pulled directly from the database.

    The enrichment uses the following mappings:
      - `item_code_1c` → DeclaredItem.item_code_1c
      - `ordinal_number` → DeclaredItem.ordinal_number
      - `declaration_number` → Declaration.declaration_number

    Args:
        order_id (int):
            ID of the Order; follows the chain Order → Container → Declaration → DeclaredItem.
        root_scp_unv (int):
            Root UNV code of the specification to start building the component tree from.
        count (float, optional):
            Quantity multiplier for calculating absolute quantities. Defaults to 1.0.
        max_depth (Optional[int], optional):
            Maximum recursion depth. `None` means no limit. Defaults to `None`.
        tv (bool, optional):
            If `True`, verifies that at least one component with a `nomsign` starting
            with `"638111111"` (i.e., a TV panel) is present. Defaults to `False`.

    Returns:
        List[Dict[str, Any]]:
            A list of dictionaries, each combining the fields from the flat component tree
            with two additional keys:
            - `row_number` (Optional[int]): The ordinal number from DeclaredItem.
            - `nom_reg`    (Optional[str]): The customs registration number from Declaration.

    Raises:
        PanelError:
            If `tv=True` and no TV panel components are found in the result.
    """
    # 1) строим базовое дерево компонентов
    components = fetch_vznab_stock_flat_tree(root_scp_unv, max_depth, count)

    # 2) вытягиваем из БД все DeclaredItem для данного order_id
    di_qs = DeclaredItem.objects.select_related('declaration', 'declaration__container') \
        .filter(declaration__container__order_id=order_id)

    lookup_row:    Dict[str, int] = {}
    lookup_nomreg: Dict[str, str] = {}
    for di in di_qs:
        if di.item_code_1c is None:
            continue
        key = str(di.item_code_1c)
        # первый встретившийся ordinal_number
        lookup_row.setdefault(key, di.ordinal_number)
        # первый встретившийся declaration_number
        lookup_nomreg.setdefault(key, di.declaration.declaration_number)

    enriched: List[Dict[str, Any]] = []
    panel_found = False

    for item in components:
        nomsign = item.get("nomsign")
        if tv and isinstance(nomsign, str) and nomsign.startswith("638111111"):
            panel_found = True

        key = str(nomsign) if nomsign is not None else None
        row_number = lookup_row.get(key)
        nom_reg    = lookup_nomreg.get(key)

        # отбрасываем, если нет ни позиции, ни номера ГТД
        if row_number is None and nom_reg is None:
            continue

        enriched.append({
            **item,
            "row_number": row_number,
            "nom_reg":    nom_reg,
        })

    if tv and not panel_found:
        logger.warning(f"No panel items for TV model {root_scp_unv}, order {order_id}")
        raise PanelError(f"Panel components not found for TV model {root_scp_unv}")

    return enriched


def clear_order_items(
    order_number: int,
    model: int,
    quantity: float,
    is_tv: bool = False,
) -> List[Dict[str, Any]]:
    """
    Perform the “clear items” process:
    1. Fetch component list with row_number and nom_reg.
    2. For each, match DeclaredItem, decrement available_quantity, write ClearedItem.
    3. Return a list of dicts with item name, expected, actual, missing, message (if any).

    Raises:
        PanelError: if is_tv=True and no panel components found.
        Any exception from fetch_stock_tree_with_row_numbers will bubble up.
    """
    fetched = fetch_stock_tree_with_row_numbers(order_number, model, quantity, is_tv)
    results: List[Dict[str, Any]] = []

    # Wrap DB updates in a transaction
    with transaction.atomic():
        for item in fetched:
            row_number = item["row_number"]
            nom_reg    = item["nom_reg"]
            abs_qty    = item["absolute_quantity"]
            name       = item["name"]

            try:
                di = DeclaredItem.objects.select_for_update().select_related("declaration").get(
                    ordinal_number=row_number,
                    declaration__declaration_number=nom_reg
                )
            except DeclaredItem.DoesNotExist:
                logger.warning(
                    f"DeclaredItem not found for row={row_number}, declaration={nom_reg}"
                )
                results.append({
                    "item":    name,
                    "expected": abs_qty,
                    "actual":   0.0,
                    "missing":  abs_qty,
                    "message": "Declared item not found"
                })
                continue

            available = di.available_quantity or 0.0
            to_clear  = min(abs_qty, available)

            # Decrement available_quantity
            di.available_quantity = available - to_clear
            di.save(update_fields=["available_quantity"])

            # Create ClearedItem if anything to clear
            if to_clear > 0:
                ClearedItem.objects.create(
                    product_id=int(model),
                    declared_item_id=di,
                    quantity=to_clear
                )

            results.append({
                "item":     name,
                "expected": abs_qty,
                "actual":   to_clear,
                "missing":  max(0.0, abs_qty - to_clear),
            })

    return results
