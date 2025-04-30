import logging
from datetime import datetime
from typing import List, Dict

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from apps.arrival.models import Order
from apps.declaration.models import Declaration


logger = logging.getLogger(__name__)


class OrderNotFoundError(Exception):
    """Raised when the given Order ID does not exist."""
    pass


class Api1CError(Exception):
    """Raised when the API 1C request fails or returns an error response."""
    pass


def fetch_declarations_from_1c(order_id: int) -> List[Dict]:
    """
    Fetch declaration details from the 1C API for all Declarations linked to an Order.

    Args:
        order_id (int): Primary key of the Order model.

    Returns:
        List[Dict]: List of records as returned by the 1C API.

    Raises:
        OrderNotFoundError: If no Order exists with the given ID.
        Api1CError: If the HTTP request fails or the API returns a non-200 status.
    """
    # Validate Order existence
    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        logger.error(f"Order with ID {order_id} not found.")
        raise OrderNotFoundError(f"Order with ID {order_id} not found.")

    # Gather linked Declarations via Containers
    declarations_qs = Declaration.objects.filter(
        container__order=order
    ).values('declaration_number', 'declaration_date')

    declarations_payload = []
    for decl in declarations_qs:
        # Format date as YYYYMMDD
        date_formatted = decl['declaration_date'].strftime('%Y%m%d')
        declarations_payload.append({
            'number': decl['declaration_number'],
            'date': date_formatted,
        })

    # If there are no declarations, return empty list
    if not declarations_payload:
        logger.info(f"No declarations found for Order ID {order_id}.")
        return []

    # Prepare API request
    api_url = getattr(settings, 'API_URL', 'http://192.168.2.2/VITYAS-2/hs/bloom/data/')
    username = settings.API_USERNAME
    password = settings.API_PASSWORD
    body = {'declarations': declarations_payload}

    try:
        response = requests.get(
            api_url,
            json=body,
            auth=(username, password),
            timeout=10,  # seconds
        )
    except requests.RequestException as exc:
        logger.exception("Failed to connect to 1C API.")
        raise Api1CError(f"Failed to connect to 1C API: {exc}")

    if response.status_code != 200:
        logger.error(
            f"1C API returned status {response.status_code}: {response.text}"
        )
        raise Api1CError(
            f"1C API error {response.status_code}: {response.text}"
        )

    try:
        data = response.json()
    except ValueError:
        logger.error("Invalid JSON in 1C API response.")
        raise Api1CError("Invalid JSON response from 1C API.")

    return data
