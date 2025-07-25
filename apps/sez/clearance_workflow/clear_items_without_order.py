import logging
from typing import List, Dict, Any

from django.db import transaction

from apps.declaration.models import DeclaredItem
from apps.sez.clearance_workflow.vznab_stock_service import (
    fetch_vznab_stock_flat_tree, PanelError
)
from apps.sez.models import ClearedItem, ClearanceInvoiceItems

logger = logging.getLogger(__name__)


def clear_model_items(
    model_code: int,
    quantity: float,
    invoice_item_id: int,
    is_tv: bool = False,
) -> List[Dict[str, Any]]:
    """
    Recursively fetch the component breakdown for a given model and clear items from
    available declared stock, writing ClearedItem records and updating available_quantity.
    Binds created ClearedItem entries to the given invoice_item.clearance_invoice.

    Args:
        model_code (int):
            UNV code of the root specification to clear.
        quantity (float):
            Total quantity of the root model to clear (will be multiplied through component tree).
        invoice_item_id (int):
            ID of the ClearanceInvoiceItems triggering this clearance; used to set ClearedItem.clearance_invoice.
        is_tv (bool, optional):
            If True, verifies that at least one component represents a TV panel (nomsign starts
            with '638111111'); otherwise raises PanelError. Defaults to False.

    Returns:
        List[Dict[str, Any]]: A list of results per component, each dictionary containing:
            - name (str): DeclaredItem.name of the cleared product.
            - requested (float): Total quantity requested to clear for this component.
            - plan (List[Dict[str, float]]): Breakdown of cleared quantities by declaration.
            - not_cleared (float): Quantity that could not be cleared due to insufficient stock.

    Raises:
        PanelError: If is_tv=True and no TV panel component is found in the breakdown.
    """
    # Retrieve the invoice item instance
    invoice_item = ClearanceInvoiceItems.objects.get(pk=invoice_item_id)

    # 1) Fetch flat component tree with absolute quantities
    components = fetch_vznab_stock_flat_tree(model_code, None, quantity)
    logger.debug(f'Fetched component tree for model {model_code}')

    # 2) Optional TV panel check
    if is_tv:
        if not any(
            isinstance(item.get("nomsign"), str) and item["nomsign"].startswith("638111111")
            for item in components
        ):
            logger.warning(f"No TV panel components found for model {model_code}")
            raise PanelError(f"Panel components not found for TV model {model_code}")

    results: List[Dict[str, Any]] = []

    # 3) Clear each component against DeclaredItem stocks
    with transaction.atomic():
        for item in components:
            nomsign = item.get("nomsign")
            if not nomsign:
                continue

            try:
                code_1c = int(nomsign)
            except (TypeError, ValueError):
                logger.warning(f"Skipping component with invalid 1C code: {nomsign}")
                continue

            requested_qty = item.get("absolute_quantity", 0.0)
            if requested_qty <= 0:
                continue

            di_qs = (
                DeclaredItem.objects.select_for_update()
                .select_related("declaration")
                .filter(item_code_1c=code_1c, available_quantity__gt=0.0, declaration__gifted=False)
                .order_by('item_code_1c', "declaration__declaration_date")
            )

            plan: List[Dict[str, Any]] = []
            remaining = requested_qty
            product_name: str = ""

            for di in di_qs:
                available = di.available_quantity or 0.0
                if available <= 0:
                    continue

                to_clear = min(available, remaining)
                if not product_name:
                    product_name = di.name

                # Update available_quantity
                di.available_quantity = available - to_clear
                di.save(update_fields=["available_quantity"])

                # Record clearance
                ClearedItem.objects.create(
                    product_id=model_code,
                    clearance_invoice=invoice_item.clearance_invoice,
                    clearance_invoice_items=invoice_item,
                    declared_item_id=di,
                    quantity=to_clear,
                )

                plan.append({
                    "declaration_number": di.declaration.declaration_number,
                    "cleared": to_clear,
                })

                remaining -= to_clear
                if remaining <= 0:
                    break

            # Skip if nothing was cleared for this component
            # if not plan:
            #     continue

            # Fallback product name
            if not product_name:
                product_name = item.get("name") or str(model_code)

            results.append({
                "name": product_name,
                "requested": requested_qty,
                "plan": plan,
                "not_cleared": max(0.0, remaining),
            })

    return results
