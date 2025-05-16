import logging
from typing import List, Dict, Any

from django.db import transaction

from apps.sez.clearance_workflow.vznab_stock_service import fetch_stock_tree_with_row_numbers
from apps.declaration.models import DeclaredItem
from apps.sez.models import ClearedItem

logger = logging.getLogger(__name__)


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

"""
from apps.omega.services.clear_items_service import clear_order_items
results = clear_order_items(26, 931938, 100)
for result in results:
    print(result)
"""