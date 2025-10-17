from typing import Dict, Tuple, List, Any, Optional

from django.db.models import Sum, F, FloatField, ExpressionWrapper, Subquery, OuterRef
from django.db import transaction

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.shtrih.models import Products, Models, Consignments
from apps.declaration.models import Declaration
from apps.omega.models import VzNab, Stockobj, VzNorm
from apps.sez.clearance_workflow.calculate.update_item_codes_1c import update_item_codes_1c
from apps.sez.clearance_workflow.calculate.omega_fetch import fetch_vznab_stock_flat_tree
from apps.sez.exceptions import (
    InvoiceNotFoundException,
    InvoiceAlreadyClearedException,
    ProductsNotEnoughException,
    InternalException,
    OracleException,
)


def begin_calculation(invoice_id: int, order_id: int, is_gifted: bool, only_panel: bool):
    '''
    Начинаем рассчет по invoice_id
    '''
    # проверка invoice
    invoice = ClearanceInvoice.objects.filter(id=invoice_id).first()
    if not invoice:
        raise InvoiceNotFoundException()
    if invoice.cleared:
        raise InvoiceAlreadyClearedException()

    # обновляем пустые declared_item.item_code_1c
    update_item_codes_1c()

    invoice_items = ClearanceInvoiceItems.objects.filter(
        clearance_invoice=invoice, declared_item__isnull=True)

    with transaction.atomic():
        all_products = []
        for item in invoice_items:
            # возвращает - "model_id": int - "model_display": str (СКЖИ)- "count": int - "unvcode": int is_tv: bool
            # и список products в n количестве со самых старых
            used_models, product_list = process_product(item, order_id, is_gifted)

            all_products.extend(product_list)


def process_product(invoice_item: ClearanceInvoiceItems, order_id: int, is_gifted: bool) -> Tuple:
    '''
    Получаем список product c фильтрацией по условиям
    Получаем список моделей из этих product
    Получаем СКЖИ и unv_code из stockobj по этим моделям

    Args:
        invoice_item (ClearanceInvoiceItems): ClearanceInvoiceItems object to process.
        order_id (int): PK of the Order to process or None
        is_gifted (bool): use gifted declaration or not

    Returns:
        typle(
            list(dict{: One dict per distinct model, e.g.:
            [
              {"model_id": 5377, "model_display": "СКЖИ.463237.173-И", "count": 5, unvcode: 931684, is_tv: True},
              {"model_id": 456, "model_display": "B789",  "count": 3, unvcode: 931684, is_tv: True},
            ]
            })
            list[products]
        )
    '''
    # Получаем список products с фильтрацией по условиям
    products = Products.objects.filter(model__name__id=invoice_item, cleared__isnull=True)
    if order_id:
        # get list of decl in order: [('07260/52003398',), ('07260/52001406',), ('07260/52001405',), ('07260/52001449',), ('07260/52001402',)]
        declaration_numbers = Declaration.objects.filter(
            container__order__id=order_id).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    if is_gifted:
        declaration_numbers = Declaration.objects.filter(gifted=True).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    else:
        declaration_numbers = Declaration.objects.filter(
            gifted=False).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    products = products.order_by('id')

    # Ошибка нехватки количества товаров
    request_quantity = invoice_item.quantity
    products_quantity = products.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    if request_quantity > products_quantity:
        raise ProductsNotEnoughException(
            f'Недостаточно товаров для списания. Требуется: {request_quantity}, есть: {products_quantity}'
        )

    # Получаем скисок products с нужным колличеством
    products_list = list(products[:request_quantity])

    # Считаем количество моделей в products_list
    models_quantity: Dict[int:int] = dict()
    for prod in products_list:
        mid = prod.model_id
        models_quantity[mid] = models_quantity.get(mid, 0) + 1

    # Делаем словарь СКЖИ по всем моделям
    models = Models.objects.filter(id__in=models_quantity.keys()).only(
        'id', 'letter_part', 'numeric_part', 'execution_part', 'production_code'
    )
    if not models:
        raise InternalException('Не найдены модели в products_list')
    model_display_map: Dict[int, str] = {
        m.id: f"{m.letter_part}{m.numeric_part}{m.execution_part or ''}"  # СКЖИ
        for m in models
    }
    is_tv = True
    if models[0].production_code != 400:
        is_tv = False

    # Омега, получаем unv_code из stockobj через signs (СКЖИ)
    # unv_code = код изделия
    signs = list({model_display_map[mid] for mid in models_quantity})
    stockobjs = (
        Stockobj.objects
        .using('oracle_db')
        .filter(sign__in=signs)
        .values('sign', 'unvcode')
    )
    sign_to_unv = {s['sign']: s['unvcode'] for s in stockobjs}

    results: List[Dict[str, Any]] = []
    for mid, cnt in models_quantity.items():
        disp = model_display_map[mid]
        results.append({
            "model_id": mid,
            "model_display": disp,
            "count": float(cnt),
            "unvcode": int(sign_to_unv.get(disp)),
            "is_tv": is_tv,
        })

    return results, products_list



