import logging

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.sez.models import (
    ClearanceInvoiceItems,
    ClearanceInvoiceItemModels,
)
from apps.shtrih.models import Models

logger = logging.getLogger(__name__)


def attach_unv_models_to_invoice_item(invoice_item_id: int) -> None:
    """
    Given the ID of a ClearanceInvoiceItems record, find all Models
    whose `name_id` matches that item's `model_name_id` and create
    many-to-many links via the through table.

    Args:
        invoice_item_id (int):
            Primary key of the ClearanceInvoiceItems instance.

    Returns:
        None

    Raises:
        ValueError:
            If no ClearanceInvoiceItems with the given ID exists.
    """
    try:
        invoice_item = ClearanceInvoiceItems.objects.get(pk=invoice_item_id)
    except ObjectDoesNotExist:
        logger.warning(f"ClearanceInvoiceItems with id={invoice_item_id} not found")
        raise ValueError(f"ClearanceInvoiceItems with id={invoice_item_id} not found")

    model_name = invoice_item.model_name_id
    if model_name is None:
        logger.debug(f"InvoiceItem #{invoice_item_id} has no model_name_id, skipping.")
        return

    # Retrieve all shtrih.Models with the same name_id
    related_models = Models.objects.filter(name=model_name)

    # Use a transaction to ensure consistency
    with transaction.atomic():
        for mdl in related_models:
            obj, created = ClearanceInvoiceItemModels.objects.get_or_create(
                clearance_invoice_item=invoice_item,
                model=mdl,
            )
            if created:
                logger.debug(
                    f"Linked InvoiceItem #{invoice_item_id} → Model code={mdl.code}"
                )
