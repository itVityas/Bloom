from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.sez.exceptions import (
    InvoiceNotFoundException,
    InvoiceAlreadyClearedException,
)
from apps.shtrih.models import Products
from apps.sez.clearance_workflow.calculate.update_item_codes_1c import update_item_codes_1c
from apps.declaration.models import Declaration


def begin_calculation(invoice_id, order_id, is_gifted, only_panel):
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
    for item in invoice_items:
        product_list = process_product(item, order_id, is_gifted, only_panel)


def process_product(invoice_item, order_id, is_gifted, only_panel):
    '''
    Обрабатываем товар из invoice_item
    '''
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
