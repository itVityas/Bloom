import logging
from typing import List, Dict, Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db import transaction

from apps.sez.models import ClearanceInvoiceItems
from apps.shtrih.models import Models, Products

logger = logging.getLogger(__name__)


class NotEnoughProductsError(Exception):
    """Raised when there are fewer available products than requested."""
    pass


def process_products_for_invoice_item(
    invoice_item_id: int,
) -> List[Dict[str, Any]]:
    """
    1) Given the PK of a ClearanceInvoiceItems, load its related Models via the
       M2M `models_unv` (through ClearanceInvoiceItemModels).
    2) For each related Models instance, build a display string:
          letter_part + numeric_part + (execution_part or '').
    3) From Products, select `request_quantity` rows where:
         - Products.model in the set of those Models IDs
         - Products.cleared IS NULL
       ordered by ascending PK (oldest first).
       If there are fewer than `request_quantity`, raise NotEnoughProductsError.
    4) Count how many of the pulled Products belong to each Models ID.
    5) Return a list of dicts, each with:
         - "model_id": int
         - "model_display": str
         - "count": int

    Args:
        invoice_item_id (int): PK of the ClearanceInvoiceItems to process.

    Returns:
        List[Dict[str, Any]]: One dict per distinct model, e.g.:
            [
              {"model_id": 123, "model_display": "A123X", "count": 5},
              {"model_id": 456, "model_display": "B789",  "count": 3},
            ]

    Raises:
        ObjectDoesNotExist:
            If no ClearanceInvoiceItems with given ID exists.
        NotEnoughProductsError:
            If available Products (cleared IS NULL) < request_quantity.
    """
    # 1) Load the invoice item and its related Models
    try:
        invoice_item = ClearanceInvoiceItems.objects.get(pk=invoice_item_id)
    except ClearanceInvoiceItems.DoesNotExist:
        raise ObjectDoesNotExist(f"ClearanceInvoiceItems #{invoice_item_id} not found")

    request_quantity = int(invoice_item.quantity)
    related_models_qs = invoice_item.models_unv.all().only(
        'id', 'letter_part', 'numeric_part', 'execution_part'
    )

    # Build a mapping model_id → display string
    model_display_map: Dict[int, str] = {
        m.id: f"{m.letter_part}{m.numeric_part}{m.execution_part or ''}"
        for m in related_models_qs
    }
    model_ids = list(model_display_map.keys())

    if not model_ids:
        # Нечего списывать
        return []

    # 2) Fetch requested Products
    products_qs = (
        Products.objects
        .filter(model_id__in=model_ids, cleared__isnull=True)
        .order_by('id')  # oldest first
    )

    # We only need the first N items
    products_list = list(products_qs[:request_quantity])

    if len(products_list) < request_quantity:
        raise NotEnoughProductsError(
            f"Requested {request_quantity} products, but only "
            f"{len(products_list)} available."
        )

    # 3) Count per model
    counts: Dict[int, int] = {}
    for prod in products_list:
        mid = prod.model_id
        counts[mid] = counts.get(mid, 0) + 1

    # 4) Build result list
    results: List[Dict[str, Any]] = []
    for mid, cnt in counts.items():
        results.append({
            "model_id": mid,
            "model_display": model_display_map.get(mid, str(mid)),
            "count": cnt,
        })

    return results
