import logging
from typing import List, Dict, Optional, Set

from django.db import DatabaseError
from django.db.models import F, FloatField, ExpressionWrapper, Subquery, OuterRef

from apps.omega.models import VzNab, Stockobj

logger = logging.getLogger(__name__)


class VzNabNotFoundError(Exception):
    """Raised when there are no VzNab entries for the given specification."""
    pass


class OracleDBError(Exception):
    """Raised on Oracle DB errors."""
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
        root_scp_unv (int): UNV code of the root specification.
        max_depth (Optional[int]): Maximum recursion depth. None means unlimited.

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
            logger.warning(f"Cycle detected at {scp_unv}, skipping this node.")
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
