from rest_framework import serializers

from apps.sez.models import ClearanceUncleared


class ClearanceUnclearedSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    model_name = serializers.CharField(
        source='invoice_item.model_name_id.name'
    )

    class Meta:
        model = ClearanceUncleared
        fields = [
            'model_name',
            'name',
            'request_quantity',
            'uncleared_quantity',
            'reason',
            'comment',
        ]
