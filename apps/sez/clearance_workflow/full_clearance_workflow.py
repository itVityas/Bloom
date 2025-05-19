import logging
from typing import List, Dict, Any

from apps.sez.clearance_workflow.clear_items_without_order import clear_model_items
from apps.sez.clearance_workflow.shtrih_service import process_products_for_invoice_item, \
    mark_products_cleared
from apps.sez.clearance_workflow.independent.update_item_codes_1c import update_item_codes_1c
from apps.sez.models import ClearanceInvoiceItems
from apps.shtrih.models import Products

logger = logging.getLogger(__name__)


def execute_full_clearance_workflow(
    invoice_id: int,
    is_tv: bool = False,
) -> List[Dict[str, Any]]:
    """
    Process a ClearanceInvoice by clearing items for each
    ClearanceInvoiceItems without declared_item.

    Args:
        invoice_id (int):
            ID of the ClearanceInvoice to process.
        is_tv (bool, optional):
            Passed through to clear_model_items for TV panel checks.

    Returns:
        List[Dict[str, Any]]: Aggregated results from clear_model_items calls.
    """

    # Update all fields where item_code_1c is NULL in DeclaredItem
    update_item_codes_1c()

    items_qs = ClearanceInvoiceItems.objects.filter(
        clearance_invoice_id=invoice_id,
        declared_item__isnull=True
    )
    all_results: List[Dict[str, Any]] = []
    products_for_cleared: List[Products] = []

    for invoice_item in items_qs:
        used_models, product_list = process_products_for_invoice_item(invoice_item.id)
        for m in used_models:
            results = clear_model_items(
                model_code=m.get('unvcode'),
                quantity=m.get('count'),
                invoice_item_id=invoice_item.id,
                is_tv=is_tv,
            )
            all_results.extend(results)
        products_for_cleared.extend(product_list)
    mark_products_cleared(products_for_cleared)
    return all_results