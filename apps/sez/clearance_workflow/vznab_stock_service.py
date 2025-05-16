import logging
from typing import List, Dict, Optional, Set, Any

from django.db import DatabaseError
from django.db.models import F, FloatField, ExpressionWrapper, Subquery, OuterRef

from apps.declaration.models import DeclaredItem
from apps.omega.models import VzNab, Stockobj, VzNorm

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
    count: float = 1.0,
) -> List[Dict[str, Optional[object]]]:
    """
    Fetch a flat list of all components for a given specification (root_scp_unv),
    recursively expanding only items whose item_sign starts with 'СКЖИ'.
    Also for each 'СКЖИ' node adds related VzNorm entries.

    Args:
        root_scp_unv (int): UNV code of the root specification
        max_depth (Optional[int]): Maximum recursion depth. None means unlimited
        count (int): Number of items for calculation total count

    Returns:
        List[Dict]: Each dict has keys:
            - scp_unv: int
            - item_sign: str
            - item_unv: int
            - quantity: float
            - name: str
            - nomsign: str | None
            - absolute_quantity: float
    """
    flat_list: List[Dict[str, Optional[object]]] = []
    visited: Set[int] = set()

    norm_nomsign_sq = Subquery(
        Stockobj.objects.using('oracle_db')
        .filter(basecode=OuterRef('mat_code_id'))
        .values('nomsign')[:1]
    )

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
            return

        for item in items:
            abs_qty = item['quantity'] * parent_qty
            flat_list.append({
                **item,
                'absolute_quantity': abs_qty,
            })

            if isinstance(item['item_sign'], str) and item['item_sign'].startswith('СКЖИ'):
                norms_qs = (
                    VzNorm.objects.using('oracle_db')
                    .filter(unvcode_id=item['item_unv'])
                    .select_related('mat_code')
                    .annotate(stock_nomsign=norm_nomsign_sq)
                )
                for norm in norms_qs:
                    norm_qty = float(norm.norm or 0.0)
                    norm_abs = norm_qty * parent_qty

                    flat_list.append({
                        'scp_unv': item['item_unv'],         # родительский unv
                        'item_sign': norm.plcode,            # vz_norm.plcode
                        'item_unv': norm.mat_code_id,        # vz_norm.mat_code
                        'quantity': norm_qty,                # vz_norm.norm
                        'name': norm.mat_code.name,          # materials.name
                        'nomsign': norm.stock_nomsign,       # stockobj.nomsign
                        'absolute_quantity': norm_abs,
                    })

                # 3) Рекурсивно спускаемся дальше по СКЖИ
                recurse(
                    item['item_unv'],
                    abs_qty,
                    (depth - 1) if depth is not None else None,
                )

    recurse(root_scp_unv, parent_qty=count, depth=max_depth)
    return flat_list
