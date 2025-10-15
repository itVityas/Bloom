# apps/sez/serializers/full_clearance_workflow.py

from rest_framework import serializers


class ClearanceDeleteInputSerializer(serializers.Serializer):
    """
    Serializer for input data to the full clearance workflow endpoint.

    Fields:
        invoice_id (int): ID of the ClearanceInvoice to process
        is_tv (bool): Whether to enforce TV‑panel checks
    """
    invoice_id = serializers.IntegerField(
        help_text="ID of the ClearanceInvoice to process."
    )


class ClearanceCalculateInputSerializer(serializers.Serializer):
    """
    Serializer for input data to the full clearance workflow endpoint.

    Fields:
        invoice_id (int): ID of the ClearanceInvoice to process
        is_tv (bool): Whether to enforce TV‑panel checks
    """
    invoice_id = serializers.IntegerField(
        help_text="ID of the ClearanceInvoice to process."
    )
    order_id = serializers.IntegerField(
        required=False,
        help_text="ID of the Order to process."
    )
    is_gifted = serializers.BooleanField(
        default=False,
        help_text="Whether the order is gifted."
    )
    only_panel = serializers.BooleanField(
        default=False,
        help_text="Whether to process only the panel."
    )
