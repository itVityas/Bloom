from typing import Dict, Tuple, List, Any

from django.db.models import Sum
from django.db import transaction
from django.utils import timezone

from apps.sez.models import (
    ClearanceInvoice,
    ClearanceInvoiceItems,
    ClearedItem,
    ClearanceUncleared
)
from apps.shtrih.models import Products, Models
from apps.declaration.models import Declaration, DeclaredItem
from apps.omega.models import Stockobj
from apps.sez.clearance_workflow.calculate.update_item_codes_1c import update_item_codes_1c
from apps.sez.clearance_workflow.calculate.omega_fetch import component_flat_list
from apps.sez.exceptions import (
    InvoiceNotFoundException,
    InvoiceAlreadyClearedException,
    ProductsNotEnoughException,
    InternalException,
    PanelException,
)


def clear_model_items(
                        invoice_item: ClearanceInvoiceItems,
                        model_code: int,
                        quantity: float,
                        is_tv: bool,
                        gifted: bool,
                        only_panel: bool) -> List[Dict[str, Any]]:
    '''
    Args:
        invoice_item (ClearanceInvoiceItems):
            Object of the ClearanceInvoiceItems triggering this clearance; used to set ClearedItem.clearance_invoice.
        model_code (int):
            UNV code of the root specification to clear.
        quantity (float):
            Total quantity of the root model to clear (will be multiplied through component tree).
        is_tv (bool):
            If True, verifies that at least one component represents a TV panel (nomsign starts
            with '638111111'); otherwise raises PanelError. Defaults to False.
        gifted (bool): false - use not gifted, true use only gifted declaration items
        only_panel (bool): false use all components, true use only panel (need is_tv true)

    Returns:
        List[Dict[str, Any]]: A list of results per component, each dictionary containing:
            - name (str): DeclaredItem.name of the cleared product.
            - requested (float): Total quantity requested to clear for this component.
            - plan (List[Dict[str, float]]): Breakdown of cleared quantities by declaration.
            - not_cleared (float): Quantity that could not be cleared due to insufficient stock.

    Raises:
        PanelError: If is_tv=True and no TV panel component is found in the breakdown.
    '''
    components = component_flat_list(model_code, None, quantity)

    # find in TV components panel or Exception
    if is_tv:
        if not any(
            isinstance(item.get("nomsign"), str) and item["nomsign"].startswith("638111111")
            for item in components
        ):
            raise PanelException(f"Panel components not found for TV model {model_code}")

    # clear each component against DeclaredItem stocks
    for item in components:
        nomsign = item.get('nomsign', None)
        if not nomsign:
            continue

        if only_panel and is_tv:
            if not isinstance(item.get("nomsign"), str) or not item["nomsign"].startswith("638111111"):
                continue

        try:
            code_1c = int(nomsign)
        except (TypeError, ValueError):
            continue

        requested_qty = item.get('absolute_quantity', 0.0)
        if requested_qty <= 0:
            continue

        di_qs = (
                DeclaredItem.objects.select_for_update()
                .select_related("declaration")
                .filter(item_code_1c=code_1c, available_quantity__gt=0.0, declaration__gifted=gifted)
                .order_by('item_code_1c', "declaration__declaration_date")
            )

        remaining = requested_qty

        for di in di_qs:
            available = di.available_quantity or 0.0
            if available <= 0:
                continue

            to_clear = min(available, remaining)

            # Update available_quantity
            di.available_quantity = available - to_clear
            di.save(update_fields=["available_quantity"])

            # Record clearance
            ClearedItem.objects.create(
                clearance_invoice_items=invoice_item,
                declared_item_id=di,
                quantity=to_clear,
            )

            remaining -= to_clear
            if remaining <= 0:
                break

        if di_qs.count() == 0 and remaining > 0:
            ClearanceUncleared.objects.create(
                invoice_item=invoice_item,
                name=nomsign,
                request_quantity=requested_qty,
                uncleared_quantity=requested_qty,
                reason="No matching declaration items",
            )
            continue

        if remaining > 0:
            ClearanceUncleared.objects.create(
                invoice_item=invoice_item,
                name=nomsign,
                request_quantity=requested_qty,
                uncleared_quantity=remaining,
                reason="Not enough stock",
            )
            continue


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
        for item in invoice_items:
            # возвращает - "model_id": int - "model_display": str (СКЖИ)- "count": int - "unvcode": int is_tv: bool
            # и список products в n количестве со самых старых
            used_models, product_list = process_product(item, order_id, is_gifted)

            for m in used_models:
                clear_model_items(
                    invoice_item=item,
                    model_code=m.get('unvcode'),
                    quantity=m.get('count'),
                    is_tv=m.get('is_tv'),
                    gifted=is_gifted,
                    only_panel=only_panel
                )

            # обновляем запись в продуктах
            for product in product_list:
                product.cleared = invoice
                product.save(update_fields=['cleared'])

        # помечаем инвойс как рассчитанный
        invoice.cleared = True
        invoice.date_calc = timezone.now()
        invoice.save()


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
    products = Products.objects.filter(model__name__id=invoice_item.model_name_id.id, cleared__isnull=True)
    if order_id:
        # get list of decl in order: [('07260/52003398',), ('07260/52001406',),
        # ('07260/52001405',), ('07260/52001449',), ('07260/52001402',)]
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
    products_quantity = products_quantity or 0.0
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
