import logging
from typing import List, Dict, Optional, Set, Any

from django.db import DatabaseError
from django.db.models import F, FloatField, ExpressionWrapper, Subquery, OuterRef

from apps.omega.models import VzNab, Stockobj
from apps.omega.services.api_1c_service import fetch_declarations_from_1c, Api1CError

logger = logging.getLogger(__name__)


class VzNabNotFoundError(Exception):
    """Raised when there are no VzNab entries for the given specification."""
    pass


class OracleDBError(Exception):
    """Raised on Oracle DB errors."""
    pass


class PanelError(Exception):
    """Raised if Panel declarations not have panel."""
    pass


def fetch_vznab_stock_details(scp_unv: int) -> List[Dict[str, Optional[object]]]:
    """
    Fetch joined data from VzNab, Konstrobj (via item_unv), and Stockobj (via unvcode).

    Args:
        scp_unv (int): Primary key of Konstrobj for specification (field VzNab.spc_unv).

    Returns:
        List[Dict]: List of records with keys:
            - scp_unv: int
            - item_sign: str
            - item_unv: int
            - quantity: float (cntnum / cntdenom)
            - name: str (Konstrobj.name)
            - nomsign: str (Stockobj.nomsign or None)

    Raises:
        OracleDBError: On database errors.
    """
    try:
        stock_nomsign_sq = Subquery(
            Stockobj.objects.using('oracle_db')
            .filter(unvcode=OuterRef('item_unv__unvcode'))
            .values('nomsign')[:1]
        )

        qs = (
            VzNab.objects.using('oracle_db')
            .filter(spc_unv_id=scp_unv)
            .select_related('item_unv')
            .annotate(
                quantity=ExpressionWrapper(
                    F('cntnum') / F('cntdenom'), output_field=FloatField()
                ),
                name=F('item_unv__name'),
                nomsign=stock_nomsign_sq
            )
        )

        raw = list(qs.values('spc_unv_id', 'item_sign', 'item_unv_id', 'quantity', 'name', 'nomsign'))
        results = [
            {
                'scp_unv': r['spc_unv_id'],
                'item_sign': r['item_sign'],
                'item_unv': r['item_unv_id'],
                'quantity': r['quantity'],
                'name': r['name'],
                'nomsign': r.get('nomsign'),
            }
            for r in raw
        ]
        return results

    except DatabaseError as exc:
        logger.exception("Oracle DB error during fetch_vznab_stock_details.")
        raise OracleDBError(f"Database error: {exc}")


def fetch_vznab_stock_flat_tree(
    root_scp_unv: int,
    max_depth: Optional[int] = None,
) -> List[Dict[str, Optional[object]]]:
    """
    Fetch a flat list of all components for a given specification (root_scp_unv),
    recursively expanding only items whose item_sign starts with 'СКЖИ'.

    Args:
        root_scp_unv (int): UNV code of the root specification
        max_depth (Optional[int]): Maximum recursion depth. None means unlimited

    Returns:
        List[Dict]: Flat list of dicts with keys:
            - scp_unv
            - item_sign
            - item_unv
            - quantity
            - name
            - nomsign
            - absolute_quantity: float

    Raises:
        OracleDBError
    """
    flat_list: List[Dict[str, Optional[object]]] = []
    visited: Set[int] = set()

    def recurse(scp_unv: int, parent_qty: float, depth: Optional[int]) -> None:
        if scp_unv in visited:
            logger.debug(f"Cycle detected at {scp_unv}, skipping this node.")
            return
        visited.add(scp_unv)

        if depth is not None and depth < 0:
            logger.debug(f"Max depth reached at {scp_unv}, stopping recursion.")
            return

        try:
            items = fetch_vznab_stock_details(scp_unv)
        except VzNabNotFoundError:
            # No entries for this spec, skip recursion
            return

        for item in items:
            abs_qty = item['quantity'] * parent_qty
            node = {
                **item,
                'absolute_quantity': abs_qty,
            }
            flat_list.append(node)

            # recurse only for items with СКЖИ prefix
            if isinstance(item.get('item_sign'), str) and item['item_sign'].startswith('СКЖИ'):
                recurse(
                    item['item_unv'],
                    abs_qty,
                    (depth - 1) if depth is not None else None,
                )

    recurse(root_scp_unv, parent_qty=1.0, depth=max_depth)
    return flat_list


def fetch_stock_tree_with_row_numbers(
    order_id: int,
    root_scp_unv: int,
    max_depth: Optional[int] = None,
    tv: Optional[bool] = False,
) -> List[Dict[str, Any]]:
    """
    Build a flat component list and enrich each item with 'row_number' and 'nom_reg'
    from 1C API by matching 'nomsign' to 'НоменклатураЗаводскойКод'.

    Args:
        order_id (int): ID of the Order for which to fetch declarations
        root_scp_unv (int): Root UNV code of specification
        max_depth (Optional[int]): Recursion depth for component expansion
        tv (Optional[bool]): If True, check panel availability in the declaration.

    Returns:
        List[Dict]: Each dict includes all fields from a flat tree plus:
            - 'row_number': Optional[int]
            - 'nom_reg': Optional[str]

    Raises:
        Api1CError: If API call fails.
    """
    components = fetch_vznab_stock_flat_tree(root_scp_unv, max_depth)
    panel = False

    try:
        api_data = fetch_declarations_from_1c(order_id)
    except Api1CError as exc:
        logger.error(f"Failed to fetch declarations for order {order_id}: {exc}")
        raise

    lookup_row: Dict[str, int] = {}
    lookup_nomreg: Dict[str, Any] = {}
    for rec in api_data:
        code = rec.get('НоменклатураЗаводскойКод')
        row = rec.get('НомерСтроки')
        nomreg = rec.get('НомерГТДКод')
        if code is not None:
            key = str(code)
            if row is not None and key not in lookup_row:
                lookup_row[key] = row
            if nomreg is not None and key not in lookup_nomreg:
                lookup_nomreg[key] = nomreg

    enriched: List[Dict[str, Any]] = []
    for item in components:
        nomsign = item.get('nomsign')
        if tv and isinstance(nomsign, str) and nomsign.startswith('638111111'):
            panel = True
        key = str(nomsign) if nomsign is not None else None
        row_number = lookup_row.get(key) if key is not None else None
        nom_reg = lookup_nomreg.get(key) if key is not None else None
        if row_number is None and nom_reg is None:
            continue
        enriched_item = {**item, 'row_number': row_number, 'nom_reg': nom_reg}
        enriched.append(enriched_item)

    if tv and not panel:
        logger.warning(f"No row numbers found for order {order_id} and TV model {root_scp_unv}")
        raise PanelError
    return enriched


"""
from apps.omega.services.vznab_stock_service import fetch_vznab_stock_flat_tree

results = fetch_vznab_stock_flat_tree(931938)
for result in results:
    print(result)
"""

"""
from apps.omega.services.vznab_stock_service import fetch_stock_tree_with_row_numbers

results = fetch_stock_tree_with_row_numbers(10, 931938)
for result in results:
    print(result)
"""
