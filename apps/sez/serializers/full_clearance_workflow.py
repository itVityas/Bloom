# apps/sez/serializers/full_clearance_workflow.py

from rest_framework import serializers


class FullClearanceWorkflowInputSerializer(serializers.Serializer):
    """
    Serializer for input data to the full clearance workflow endpoint.

    Fields:
        invoice_id (int): ID of the ClearanceInvoice to process
        is_tv (bool): Whether to enforce TV‑panel checks
    """
    invoice_id = serializers.IntegerField(
        help_text="ID of the ClearanceInvoice to process."
    )
    is_tv = serializers.BooleanField(
        default=False,
        help_text="If true, perform TV‑panel existence checks."
    )


class ClearedComponentPlanSerializer(serializers.Serializer):
    """
    Serializer for a single component’s clearance plan entry.

    Fields:
        declaration_number (str): Customs declaration registration number
        cleared (float): Quantity cleared from this declaration
    """
    declaration_number = serializers.CharField()
    cleared = serializers.FloatField()


class FullClearanceWorkflowResultSerializer(serializers.Serializer):
    """
    Serializer for one element result in the full clearance workflow.

    Fields:
        name (str): Component name
        requested (float): Quantity requested to clear
        plan (List[Dict]): List of clearance plan entries (ClearedComponentPlanSerializer)
        not_cleared (float): Quantity that could not be cleared
    """
    name = serializers.CharField()
    requested = serializers.FloatField()
    plan = serializers.ListSerializer(
        child=ClearedComponentPlanSerializer()
    )
    not_cleared = serializers.FloatField()
