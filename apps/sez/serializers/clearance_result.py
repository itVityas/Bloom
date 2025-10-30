from rest_framework import serializers

from apps.sez.models import ClearanceUncleared


class ClearanceUnclearedSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    class Meta:
        model = ClearanceUncleared
        fields = [
            'name',
            'request_quantity',
            'uncleared_quantity',
            'reason',
            'created_at',
        ]
