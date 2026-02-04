from rest_framework import serializers

from apps.sez.models import ClearedItem


class ClearedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearedItem model.
    """
    class Meta:
        model = ClearedItem
        fields = '__all__'


class ClearedItemAssemblySerializer(serializers.Serializer):
    model_name = serializers.CharField()
    total_quantity = serializers.FloatField()
    name = serializers.CharField()
    code_1c = serializers.IntegerField()
