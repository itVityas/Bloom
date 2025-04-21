import logging
from typing import List, Dict, Optional

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
        VzNabNotFoundError: If no VzNab rows found for given scp_unv.
        OracleDBError: On database errors.
    """
    try:
        # Prepare subquery for stock.nomsign based on konstrobj.unvcode
        stock_nomsign_sq = Subquery(
            Stockobj.objects.using('oracle_db')
            .filter(unvcode=OuterRef('item_unv__unvcode'))
            .values('nomsign')[:1]
        )

        # Query VzNab with related Konstrobj (item_unv) and annotate
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

        if not qs.exists():
            logger.info(f"No VzNab entries found for spec_unv={scp_unv}.")
            raise VzNabNotFoundError(f"No entries for specification {scp_unv}.")

        # Build result list
        results: List[Dict[str, Optional[object]]] = []
        for row in qs.values(
            'spc_unv_id', 'item_sign', 'item_unv_id', 'quantity', 'name', 'nomsign'
        ):
            results.append({
                'scp_unv': row['spc_unv_id'],
                'item_sign': row['item_sign'],
                'item_unv': row['item_unv_id'],
                'quantity': row['quantity'],
                'name': row['name'],
                'nomsign': row['nomsign'],
            })

        return results

    except DatabaseError as exc:
        logger.exception("Oracle DB error during fetch_vznab_stock_details.")
        raise OracleDBError(f"Database error: {exc}")
