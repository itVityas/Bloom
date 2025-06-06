import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.sez.clearance_workflow.clear_items_without_order import clear_model_items
from apps.sez.clearance_workflow.independent.update_item_codes_1c import update_item_codes_1c
from apps.sez.clearance_workflow.shtrih_service import process_products_for_invoice_item, \
    mark_products_cleared
from apps.sez.models import ClearanceInvoiceItems, ClearedItem, ClearanceInvoice, ClearanceResult
from apps.shtrih.models import Products

logger = logging.getLogger(__name__)


class AlreadyCalculatedError(Exception):
    """Raised if a ClearanceInvoice has already been processed (date_calc is set)."""
    pass


class ModelClearanceEmptyError(Exception):
    """
    Raised when clear_model_items returns no results for a given model.
    The message includes the UNV code of the model.
    """
    pass


def execute_full_clearance_workflow(invoice_id: int) -> None:
    """
    Обрабатывает ClearanceInvoice, очищает каждый ClearanceInvoiceItems,
    сохраняет результаты в таблицу ClearanceResult и устанавливает флаг расчёта.
    """

    # 1) Update all fields where item_code_1c is NULL in DeclaredItem
    update_item_codes_1c()

    # 2) Load and timestamp invoice
    try:
        invoice = ClearanceInvoice.objects.get(pk=invoice_id)
    except ClearanceInvoice.DoesNotExist:
        raise ObjectDoesNotExist(f"ClearanceInvoice #{invoice_id} not found")

    if invoice.date_calc is not None or invoice.cleared:
        raise AlreadyCalculatedError(
            f"Invoice #{invoice_id} was already calculated at {invoice.date_calc}"
        )

    # 3) Process each invoice item
    items_qs = ClearanceInvoiceItems.objects.filter(
        clearance_invoice_id=invoice_id,
        declared_item__isnull=True
    )

    with transaction.atomic():
        all_products = []
        for invoice_item in items_qs:
            used_models, product_list = process_products_for_invoice_item(invoice_item.id)

            for m in used_models:
                results = clear_model_items(
                    model_code=m.get('unvcode'),
                    quantity=m.get('count'),
                    invoice_item_id=invoice_item.id,
                    is_tv=m.get('is_tv'),
                )

                if all(not item.get('plan') for item in results):
                    raise ModelClearanceEmptyError(f'Для модели {m.get('unvcode')} не найдено ни одного материала в декларации')

                for res in results:
                    ClearanceResult.objects.create(
                        invoice_item=invoice_item,
                        name=res['name'],
                        request_quantity=res['requested'],
                        uncleared_quantity=res['not_cleared'],
                    )

            all_products.extend(product_list)

    # 4) Mark products
    mark_products_cleared(all_products, invoice_id)

    # 5) Mark invoice as calculated
    invoice.date_calc = timezone.now()
    invoice.cleared = True
    invoice.save(update_fields=['date_calc', 'cleared'])



def undo_full_clearance_workflow(invoice_id: int) -> None:
    """
    Reverse the effects of `execute_full_clearance_workflow` for a given invoice
    and clear the calculation timestamp.

    Within a single transaction:
      1. For every ClearedItem linked to this invoice:
         a. Restore DeclaredItem.available_quantity
         b. Delete the ClearedItem
      2. Reset `cleared` to NULL on all Products where cleared=invoice_id
      3. Set ClearanceInvoice.date_calc = NULL

    Args:
        invoice_id (int):
            The PK of the ClearanceInvoice to undo.

    Returns:
        None

    Raises:
        Any exception will roll back the entire transaction.
    """

    with transaction.atomic():
        # 1) Roll back declared items
        ci_qs = ClearedItem.objects.filter(clearance_invoice_id=invoice_id)
        for ci in ci_qs.select_related('declared_item_id'):
            di = ci.declared_item_id
            if di:
                di.available_quantity = F('available_quantity') + ci.quantity
                di.save(update_fields=['available_quantity'])
        ci_qs.delete()

        # 2) Reset products
        Products.objects.filter(cleared=invoice_id).update(cleared=None)

        # 3) Clear invoice timestamp
        ClearanceInvoice.objects.filter(pk=invoice_id).update(date_calc=None, cleared = False)

        # 4) Clear ClearanceResult
        ClearanceResult.objects.filter(invoice_item__clearance_invoice_id = invoice_id).delete()
