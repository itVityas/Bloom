import logging
import requests
from django.conf import settings

from apps.declaration.models import Declaration, DeclaredItem


logger = logging.getLogger(__name__)

def update_item_codes_1c():
    """
    Fetch missing item_code_1c values for declared items from the 1С API and update the database.

    Steps:
        1. Retrieve all Declarations that have at least one DeclaredItem with a null item_code_1c.
        2. Build the request payload containing declaration numbers and dates.
        3. Send a GET request to the 1C API with authentication.
        4. Parse the JSON response from the API.
        5. Match each response entry to the corresponding DeclaredItem by declaration number and line ordinal.
        6. Update the item_code_1c field for each matched DeclaredItem in bulk.
    """
    # 1. Collect declarations with missing item_code_1c
    declarations = Declaration.objects.filter(
        declared_items__item_code_1c__isnull=True
    ).distinct()
    if not declarations.exists():
        logger.info("No declarations with missing item_code_1c.")
        return

    # 2. Prepare request payload
    payload = {
        "declarations": [
            {
                "number": decl.declaration_number,
                "date": decl.declaration_date.strftime("%Y%m%d")
            }
            for decl in declarations
        ]
    }

    # 3. Send request to API
    try:
        response = requests.get(
            settings.API_1C_URL_GTD,
            json=payload,
            auth=(settings.API_USERNAME, settings.API_PASSWORD),
            timeout=30
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return

    # 4. Parse response JSON
    try:
        api_data = response.json()
    except ValueError:
        logger.error("Invalid JSON response from API")
        return

    # 5. Update DeclaredItem records
    items_to_update = []
    for entry in api_data:
        try:
            item = DeclaredItem.objects.get(
                declaration__declaration_number=entry["НомерГТДКод"],
                ordinal_number=entry["НомерСтроки"]
            )
            item.item_code_1c = int(entry["НоменклатураЗаводскойКод"])
            items_to_update.append(item)
        except DeclaredItem.DoesNotExist:
            logger.warning(
                f"DeclaredItem not found for declaration={entry['НомерГТДКод']} "
                f"line={entry['НомерСтроки']}"
            )
        except Exception as e:
            logger.error(f"Error processing API entry {entry}: {e}")

    # 6. Bulk update
    if items_to_update:
        DeclaredItem.objects.bulk_update(items_to_update, ["item_code_1c"])
        logger.info(f"Updated {len(items_to_update)} DeclaredItem records.")
