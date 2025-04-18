# apps/omega/utils/vz_nab.py

from collections import defaultdict
from typing import List, Dict, Any, Optional

from apps.omega.models import VzNab, Stockobj


def get_vz_nab_summary(
    spc_unv: int,
    order_by: str = 'pos'
) -> List[Dict[str, Optional[Any]]]:
    """
    Для заданного spc_unv возвращает список записей со следующими полями:
      - scp_unv         (int)   — из VzNab.spc_unv
      - item_sign       (str)   — из VzNab.item_sign
      - item_unv        (int)   — из VzNab.item_unv
      - quantity        (float) — cntnum / cntdenom
      - konstrobj_name  (str)   — Konstrobj.name, связанный по item_unv
      - stockobj_nomsign(str?)  — Stockobj.nomsign, найденный по sign из Konstrobj

    :param spc_unv: значение поля spc_unv в таблице VzNab
    :param order_by: поле для сортировки VzNab (по умолчанию 'pos')
    """
    # 1) Выбираем все VzNab и подтягиваем Konstrobj через FK item_unv
    vz_qs = (
        VzNab.objects
        .using('oracle_db')
        .filter(spc_unv=spc_unv)
        .select_related('item_unv')
        .order_by(order_by)
    )

    # 2) Собираем все уникальные sign из Konstrobj (item_unv.sign)
    signs = {
        vz.item_unv.sign
        for vz in vz_qs
        if vz.item_unv.sign
    }
    # Если нет ни одного sign — сразу возвращаем пустой список
    if not signs:
        return []

    # 3) Берём все Stockobj, у которых sign совпадает
    stock_qs = (
        Stockobj.objects
        .using('oracle_db')
        .filter(sign__in=signs)
    )
    # Маппинг sign -> список Stockobj
    stock_map: Dict[str, List[Stockobj]] = defaultdict(list)
    for so in stock_qs:
        stock_map[so.sign].append(so)

    # 4) Формируем итог
    result: List[Dict[str, Optional[Any]]] = []
    for vz in vz_qs:
        ko = vz.item_unv
        # Расчёт quantity, защищённо от деления на ноль
        if vz.cntdenom and vz.cntdenom != 0:
            quantity = vz.cntnum / vz.cntdenom
        else:
            quantity = None

        # Берём первый подходящий Stockobj или None
        stock_list = stock_map.get(ko.sign)
        stock_nomsign = stock_list[0].nomsign if stock_list else None

        result.append({
            'scp_unv': vz.spc_unv_id,
            'item_sign': vz.item_sign,
            'item_unv': vz.item_unv_id,
            'quantity': quantity,
            'konstrobj_name': ko.name,
            'stockobj_nomsign': stock_nomsign,
        })

    return result
