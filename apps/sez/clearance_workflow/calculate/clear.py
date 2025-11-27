import logging

from django.db import transaction
from django.db.models import F

from apps.sez.models import (
    ClearanceInvoice, ClearanceInvoiceItems, ClearedItem, ClearanceUncleared)
from apps.shtrih.models import Products
from apps.sez.exceptions import InvoiceNotFoundException

logger = logging.getLogger('apps.omega')


def clear_invoice_calculate(invoice_id: int):
    '''
    Очищаем рассчет по invoice_id
    Очищаем Products, количество в declared_item, удаляем ClearedItem и ClearanceUncleared,
    удаляем поля с рассчетом в ClearanceInvoice
    '''
    invoice = ClearanceInvoice.objects.filter(id=invoice_id)
    if not invoice.exists():
        logger.error(f'Invoice {invoice_id} not found')
        raise InvoiceNotFoundException()

    logger.info(f'Start clearing invoice {invoice_id}')
    with transaction.atomic():
        Products.objects.filter(cleared=invoice_id).update(cleared=None)
        invoice_items = ClearanceInvoiceItems.objects.filter(
            clearance_invoice=invoice_id)
        for item in invoice_items:
            di = item.declared_item
            if di and di.available_quantity is not None:
                di.available_quantity = F('available_quantity') + item.quantity
                di.save(update_fields=['available_quantity'])

        cleared_items = ClearedItem.objects.filter(clearance_invoice_items__clearance_invoice__id=invoice_id)
        for item in cleared_items:
            if item.declared_item_id and item.declared_item_id.available_quantity is not None:
                item.declared_item_id.available_quantity = F('available_quantity') + item.quantity
                item.declared_item_id.save(update_fields=['available_quantity'])
        cleared_items.delete()
        ClearanceUncleared.objects.filter(invoice_item__clearance_invoice_id=invoice_id).delete()
        ClearanceInvoice.objects.filter(pk=invoice_id).update(date_calc=None, cleared=False, responsible=None)
        logger.info(f'Invoice {invoice_id} cleared')
