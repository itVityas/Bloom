import logging
from typing import List, Dict, Any, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.omega.models import Stockobj
from apps.sez.models import ClearanceInvoiceItems
from apps.shtrih.models import Products

logger = logging.getLogger(__name__)


class NotEnoughProductsError(Exception):
    """Raised when there are fewer available products than requested."""
    pass


def process_products_for_invoice_item(
    invoice_item_id: int,
) -> Tuple[List[Dict[str, Any]], List[Products]] or None:
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
    4) Batch-load Stockobj entries to get unvcode by sign
    5) Count how many of the pulled Products belong to each Models ID.
    6) Return a list of dicts, each with:
         - "model_id": int
         - "model_display": str
         - "count": int
         - "unvcode": int

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
            If no ClearanceInvoiceItems with given ID exist.
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

    # 4) Batch-load Stockobj entries to get unvcode by sign
    signs = list({model_display_map[mid] for mid in counts})
    stockobjs = (
        Stockobj.objects
        .using('oracle_db')
        .filter(sign__in=signs)
        .values('sign', 'unvcode')
    )
    sign_to_unv = {s['sign']: s['unvcode'] for s in stockobjs}

    # 5) Build result list
    results: List[Dict[str, Any]] = []
    for mid, cnt in counts.items():
        disp = model_display_map[mid]
        results.append({
            "model_id": mid,
            "model_display": disp,
            "count": float(cnt),
            "unvcode": int(sign_to_unv.get(disp)),
        })

    return results, products_list


def mark_products_cleared(
    products: List[Products],
    cleared_value: int = 1,
) -> None:
    """
    Mark a list of Products as cleared by updating their `cleared` field.

    This function:
      1. Accepts a list of Products instances to be marked.
      2. Sets each instance’s `cleared` attribute to the provided value.
      3. Persists the change to the database using a bulk update within a transaction.

    Args:
        products (List[Products]):
            The Products instances to mark as cleared.
        cleared_value (int, optional):
            The value to assign to each Product’s `cleared` field.
            Defaults to 1.

    Returns:
        None

    Raises:
        Exception:
            Any exception during the database update will roll back all changes.
    """
    if not products:
        return

    with transaction.atomic():

        for prod in products:
            prod.cleared = cleared_value

        Products.objects.bulk_update(products, ['cleared'])
        logger.debug(f"Marked {len(products)} products as cleared={cleared_value}.")