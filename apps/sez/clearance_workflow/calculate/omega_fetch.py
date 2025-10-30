from typing import Dict, List, Optional

from django.db.models import F, FloatField, ExpressionWrapper, Subquery, OuterRef, Q
from django.utils import timezone

from apps.omega.models import VzNab, Stockobj, VzNorm, AdmissibleSubst
from apps.sez.exceptions import (
    OracleException,
)


def fetch_analog_details(nomsign: str) -> List[Dict[str, Optional[object]]]:
    """Fetch analog data from AdmissibleSubst.

    Args:
        scp_unv (int): Primary key of Konstrobj for specification (field VzNab.spc_unv).

    Returns:
        List[Dict]: List of records with keys:
            - item_sign: str
            - koef: float (cntnum / cntdenom)
            - name: str (Stockobj.name)
            - nomsign: str (Stockobj.nomsign)

    Raises:
        OracleException: On database errors.
    """
    try:
        curent_date = timezone.now().date()
        stockobj = Stockobj.objects.using('oracle_db').filter(nomsign=nomsign).first()
        analogs = AdmissibleSubst.objects.using('oracle_db').filter(
            Q(dateto__gte=curent_date) | Q(dateto__isnull=True),
            Q(datefrom__lte=curent_date) | Q(datefrom__isnull=True),
            subst=stockobj,
        )
        analogs_from = AdmissibleSubst.objects.using('oracle_db').filter(
            Q(dateto__gte=curent_date) | Q(dateto__isnull=True),
            Q(datefrom__lte=curent_date) | Q(datefrom__isnull=True),
            substfor=stockobj,
            both_flag=1,
        )

        result = list()
        for analog in analogs:
            result.append(
                {
                    'item_sign': analog.substfor.sign,
                    'koef': analog.koef,
                    'name': analog.substfor.name,
                    'nomsign': analog.substfor.nomsign,
                }
            )

        for analog in analogs_from:
            result.append(
                {
                    'item_sign': analog.subst.sign,
                    'koef': analog.koef,
                    'name': analog.subst.name,
                    'nomsign': analog.subst.nomsign,
                }
            )

        return result

    except Exception as exc:
        raise OracleException(f"Database error: {exc}")


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
        OracleException: On database errors.
    """
    try:
        stock_nomsign_sq = Subquery(
            Stockobj.objects.using('oracle_db')
            .filter(unvcode=OuterRef('item_unv__unvcode'))
            .values('nomsign')[:1]
        )

        qs = (
            VzNab.objects.using('oracle_db')
            .filter(spc_unv_id=scp_unv, kdd=None)
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

    except Exception as exc:
        raise OracleException(f"Database error: {exc}")


def fetch_vznab_stock_flat_tree(
                                scp_unv: int,
                                depth: Optional[int] = None,
                                count: float = 1.0
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
    if depth is not None and depth < 0:
        return None

    flat_list: List[Dict[str, Optional[object]]] = []
    norm_nomsign_sq = Subquery(
        Stockobj.objects.using('oracle_db')
        .filter(basecode=OuterRef('mat_code_id'))
        .values('nomsign')[:1]
    )

    items = fetch_vznab_stock_details(scp_unv)

    for item in items:
        abs_qty = item['quantity'] * count
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
                norm_abs = norm_qty * count

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
            buf_rez = fetch_vznab_stock_flat_tree(
                item['item_unv'],
                (depth - 1) if depth is not None else None,
                abs_qty,
            )
            flat_list.extend(buf_rez)

    return flat_list


def component_flat_list(
                        scp_unv: int,
                        depth: Optional[int] = None,
                        count: float = 1.0
                        ) -> List[Dict[str, Optional[object]]]:
    '''
    flat and group list of components

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
    '''
    flat_list = fetch_vznab_stock_flat_tree(scp_unv, depth, count)
    for i in range(len(flat_list)-1):
        if flat_list[i] is None or flat_list == []:
            flat_list.remove(flat_list[i])
            continue
        for j in range(i+1, len(flat_list)):
            if j < len(flat_list):
                break
            if flat_list[j] is None or flat_list[j] == []:
                flat_list.remove(flat_list[j])
                continue
            if flat_list[i]['item_sign'] == flat_list[j]['item_sign']:
                flat_list[i]['absolute_quantity'] += flat_list[j]['absolute_quantity']
                flat_list.remove(flat_list[j])
                continue
    return flat_list
