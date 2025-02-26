from rest_framework import serializers
from apps.arrival.models import ClearedItem


class ClearedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearedItem model.
    """
    class Meta:
        model = ClearedItem
        fields = '__all__'