from typing import Dict, Tuple, List, Any
import logging

from django.db.models import Sum
from django.db import transaction
from django.utils import timezone

from apps.sez.models import (
    ClearanceInvoice,
    ClearanceInvoiceItems,
    ClearedItem,
    ClearanceUncleared
)
from apps.shtrih.models import Products, Models, ProductTransitions, Consignments
from apps.declaration.models import Declaration, DeclaredItem
from apps.omega.models import Stockobj
from apps.sez.clearance_workflow.calculate.update_item_codes_1c import update_item_codes_1c
from apps.sez.clearance_workflow.calculate.omega_fetch import component_flat_list, fetch_analog_details
from apps.sez.exceptions import (
    InvoiceNotFoundException,
    InvoiceAlreadyClearedException,
    ProductsNotEnoughException,
    InternalException,
    PanelException,
)


logging = logging.getLogger('apps.omega')


def clear_model_items(
                        invoice_item: ClearanceInvoiceItems,
                        model_id: int,
                        model_code: int,
                        quantity: float,
                        is_tv: bool,
                        gifted: bool,
                        only_panel: bool,
                        order_list: list = None) -> List[Dict[str, Any]]:
    '''
    Args:
        invoice_item (ClearanceInvoiceItems):
            Object of the ClearanceInvoiceItems triggering this clearance; used to set ClearedItem.clearance_invoice.
        model_id (int):
            models.id
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
    has_panel = False

    # find in TV components panel or Exception
    if is_tv:
        if not any(
            isinstance(item.get("nomsign"), str) and item["nomsign"].startswith("638111111")
            for item in components
        ):
            logging.error(f"Panel components not found for TV model {model_code}")
            raise PanelException(f"Panel components not found for TV model {model_code}")

    # clear each component against DeclaredItem stocks
    for item in components:
        item['clear'] = False
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

        if order_list:
            declaration_numbers = Declaration.objects.filter(
                container__order__id__in=order_list, is_use=True).values_list('declaration_number')
            di_qs = (
                    DeclaredItem.objects.select_for_update()
                    .select_related("declaration")
                    .filter(item_code_1c=code_1c, available_quantity__gt=0.0,
                            declaration__gifted=gifted, declaration__declaration_number__in=declaration_numbers)
                    .order_by('item_code_1c', "declaration__declaration_date")
                )
        else:
            di_qs = (
                    DeclaredItem.objects.select_for_update()
                    .select_related("declaration")
                    .filter(item_code_1c=code_1c, available_quantity__gt=0.0, declaration__gifted=gifted)
                    .order_by('item_code_1c', "declaration__declaration_date")
                )

        remaining = requested_qty

        for i in di_qs:
            di = i
            available = di.available_quantity or 0.0
            if available <= 0:
                continue

            to_clear = min(available, remaining)

            # Получает панель из consignments
            if str(di.item_code_1c).startswith("638111111"):
                consignments = Consignments.objects.filter(
                    products__model__id=model_id).values('declaration_number', 'G32').distinct()
                decl_panel = None
                if consignments:
                    for consignment in consignments:
                        decl_panel = di_qs.filter(
                            declaration__declaration_number=consignment.get('declaration_number'),
                            ordinal_number=consignment.get('G32')
                        ).first()
                        if decl_panel:
                            break
                if decl_panel and decl_panel.available_quantity > 0:
                    di = decl_panel
                has_panel = True

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
                item['clear'] = True
                break

    # работа с аналогами
    for item in components:
        if item.get('clear', True):
            continue

        nomsign = item.get('nomsign', None)
        if not nomsign:
            continue

        if only_panel and is_tv:
            if not isinstance(item.get("nomsign"), str) or not item["nomsign"].startswith("638111111"):
                continue

        requested_qty = item.get('absolute_quantity', 0.0)
        if requested_qty <= 0:
            continue

        remaining = requested_qty

        analogs = fetch_analog_details(nomsign)
        for analog in analogs:
            try:
                code_1c = int(analog.get('nomsign', None))
            except (TypeError, ValueError):
                continue

            if order_list:
                declaration_numbers = Declaration.objects.filter(
                    container__order__id__in=order_list, is_use=True).values_list('declaration_number')
                di_qs = (
                        DeclaredItem.objects.select_for_update()
                        .select_related("declaration")
                        .filter(item_code_1c=code_1c, available_quantity__gt=0.0,
                                declaration__gifted=gifted, declaration__declaration_number__in=declaration_numbers)
                        .order_by('item_code_1c', "declaration__declaration_date")
                    )
            else:
                di_qs = (
                        DeclaredItem.objects.select_for_update()
                        .select_related("declaration")
                        .filter(item_code_1c=code_1c, available_quantity__gt=0.0, declaration__gifted=gifted)
                        .order_by('item_code_1c', "declaration__declaration_date")
                    )

            is_find = False
            for i in di_qs:
                di = i
                available = di.available_quantity or 0.0
                if available <= 0:
                    continue

                to_clear = min(available, remaining)

                # Получает панель из consignments
                if str(di.item_code_1c).startswith("638111111"):
                    consignments = Consignments.objects.filter(
                        products__model__id=model_id).values('declaration_number', 'G32').distinct()
                    decl_panel = None
                    if consignments:
                        for consignment in consignments:
                            decl_panel = di_qs.filter(
                                declaration__declaration_number=consignment.get('declaration_number'),
                                ordinal_number=consignment.get('G32')
                            ).first()
                            if decl_panel:
                                break
                    if decl_panel and decl_panel.available_quantity > 0:
                        di = decl_panel
                    has_panel = True

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
                    item['clear'] = True
                    is_find = True
                    break

            if is_find:
                break

    if is_tv and not has_panel:
        logging.error(f"Panel components not found for TV model {model_code}")
        raise PanelException(f"Panel components not found for TV model {model_code}")

    for item in components:
        if not item['clear'] and item.get('nomsign'):
            ClearanceUncleared.objects.create(
                invoice_item=invoice_item,
                name=item.get('nomsign') + ': ' + item.get('name', ''),
                request_quantity=requested_qty,
                uncleared_quantity=requested_qty,
                reason="No matching declaration items",
            )


def begin_calculation(invoice_id: int):
    '''
    Начинаем рассчет по invoice_id
    '''
    # проверка invoice
    invoice = ClearanceInvoice.objects.filter(id=invoice_id).first()
    if not invoice:
        logging.error(f'Invoice {invoice_id} not found')
        raise InvoiceNotFoundException()
    if invoice.cleared:
        logging.error(f'Invoice {invoice_id} already cleared')
        raise InvoiceAlreadyClearedException()

    orders = list(invoice.order.values_list('id', flat=True)) if invoice.order else None
    is_gifted = invoice.is_gifted
    only_panel = invoice.only_panel

    # обновляем пустые declared_item.item_code_1c
    update_item_codes_1c()

    invoice_items = ClearanceInvoiceItems.objects.filter(
        clearance_invoice=invoice, model_name_id__isnull=False)

    with transaction.atomic():
        for item in invoice_items:
            # возвращает - "model_id": int - "model_display": str (СКЖИ)- "count": int - "unvcode": int is_tv: bool
            # и список products в n количестве со самых старых
            used_models, product_list = process_product(item, orders, is_gifted)

            for m in used_models:
                clear_model_items(
                    invoice_item=item,
                    model_id=m.get('model_id'),
                    model_code=m.get('unvcode'),
                    quantity=m.get('count'),
                    is_tv=m.get('is_tv'),
                    gifted=is_gifted,
                    only_panel=only_panel,
                    order_list=orders
                )

            # обновляем запись в продуктах
            for product in product_list:
                product.cleared = invoice
                product.save(update_fields=['cleared'])

        invoice_item_decl = ClearanceInvoiceItems.objects.filter(clearance_invoice=invoice, declared_item__isnull=False)
        for item in invoice_item_decl:
            if item.quantity > item.declared_item.available_quantity:
                logging.error(f"Product {item.declared_item.name} not enough quantity")
                raise ProductsNotEnoughException(f"Product {item.declared_item.name} not enough quantity")
            item.declared_item.available_quantity = item.declared_item.available_quantity - item.quantity
            item.declared_item.save(update_fields=['available_quantity'])

        # помечаем инвойс как рассчитанный
        invoice.cleared = True
        invoice.date_calc = timezone.now()
        invoice.save()


def process_product(invoice_item: ClearanceInvoiceItems, order_list: list, is_gifted: bool) -> Tuple:
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
    logging.info(f'Start process_product with invoice:{invoice_item.id} order_id:{order_list} is_gifted:{is_gifted}')
    process_transitions_list = ProductTransitions.objects.all().values_list('old_product')
    products = Products.objects.filter(model__name__id=invoice_item.model_name_id.id, cleared__isnull=True)
    if order_list:
        # get list of decl in order: [('07260/52003398',), ('07260/52001406',),
        # ('07260/52001405',), ('07260/52001449',), ('07260/52001402',)]
        declaration_numbers = Declaration.objects.filter(
            container__order__id__in=order_list, is_use=True).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    if is_gifted:
        declaration_numbers = Declaration.objects.filter(gifted=True, is_use=True).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    else:
        declaration_numbers = Declaration.objects.filter(
            gifted=False).values_list('declaration_number')
        products = products.filter(consignment__declaration_number__in=declaration_numbers)
    products = products.exclude(pk__in=process_transitions_list)
    products = products.order_by('id')

    # Ошибка нехватки количества товаров
    request_quantity = invoice_item.quantity
    products_quantity = products.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    products_quantity = products_quantity or 0.0
    if request_quantity > products_quantity:
        logging.error(f'Not enough goods to write off. need {request_quantity}, have: {products_quantity}')
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
        logging.error(f'Not found models in products_list: {products_list}')
        raise InternalException('Не найдены модели в products_list')
    model_display_map: Dict[int, str] = {
        m.id: f"{m.letter_part}{m.numeric_part}{m.execution_part or ''}"  # СКЖИ
        for m in models
    }
    is_tv = True
    if models[0].production_code and models[0].production_code.code != 400:
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
