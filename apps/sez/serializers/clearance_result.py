from rest_framework import serializers

from apps.sez.models import ClearanceResult


class ClearanceResultSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    model_name = serializers.CharField(
        source='invoice_item.model_name_id.name'
    )

    class Meta:
        model = ClearanceResult
        fields = [
            'model_name',
            'name',
            'request_quantity',
            'uncleared_quantity',
            'reason',
            'comment',
        ]
