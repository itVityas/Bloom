from django.db import transaction
from django.db.models import F

from apps.sez.models import (
    ClearanceInvoice, ClearanceInvoiceItems, ClearedItem, ClearanceUncleared)
from apps.shtrih.models import Products
from apps.sez.exceptions import InvoiceNotFoundException


def clear_invoice_calculate(invoice_id: int):
    invoice = ClearanceInvoice.objects.filter(id=invoice_id)
    if not invoice.exists():
        raise InvoiceNotFoundException()

    with transaction.atomic():
        Products.objects.filter(cleared=invoice_id).update(cleared=None)
        invoice_items = ClearanceInvoiceItems.objects.filter(
            clearance_invoice=invoice_id).select_related('declared_item')
        for item in invoice_items:
            di = item.declared_item_id
            if di:
                di.available_quantity = F('available_quantity') + item.quantity
                di.save(update_fields=['available_quantity'])

        ClearedItem.objects.filter(clearance_invoice_items__clearance_invoice_id=invoice_id).delete()
        ClearanceUncleared.objects.filter(invoice_item__clearance_invoice_id=invoice_id).delete()
        ClearanceInvoiceItems.objects.filter(clearance_invoice_id=invoice_id).delete()
        ClearanceInvoice.objects.filter(pk=invoice_id).update(date_calc=None, cleared=False)
