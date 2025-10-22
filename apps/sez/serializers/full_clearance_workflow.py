# apps/sez/serializers/full_clearance_workflow.py

from rest_framework import serializers


class ClearanceDeleteInputSerializer(serializers.Serializer):
    """
    Serializer for input data to the full clearance workflow endpoint.

    Fields:
        invoice_id (int): ID of the ClearanceInvoice to process
    """
    invoice_id = serializers.IntegerField(
        help_text="ID of the ClearanceInvoice to process."
    )


class ClearanceCalculateInputSerializer(serializers.Serializer):
    """
    Serializer for input data to the full clearance workflow endpoint.

    Fields:
        invoice_id (int): ID of the ClearanceInvoice to process
    """
    invoice_id = serializers.IntegerField(
        help_text="ID of the ClearanceInvoice to process."
    )
