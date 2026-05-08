from rest_framework import serializers

from apps.warehouse.models import BarcodlessDo
from apps.warehouse.serializers.warehouse_ttn import WarehouseTTNGetSerializer
from apps.warehouse.serializers.barcodless_product import BarcodlessProductFullSerializer


class BarcodlessDOUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for BarcodlessDO without linked models"""
    class Meta:
        model = BarcodlessDo
        fields = "__all__"


class BarcodlessDoFullSerializer(serializers.ModelSerializer):
    """Serializer for BarcodlessDO with linked models """
    barcodless_product = BarcodlessProductFullSerializer()
    warehouse_ttn = WarehouseTTNGetSerializer()

    class Meta:
        model = BarcodlessDo
        fields = "__all__"


class BarcodlessProductCreateSerializer(serializers.Serializer):
    model_name_id = serializers.IntegerField()
    color_id = serializers.IntegerField(required=False, allow_null=True)
    warehouse_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    ttn_number = serializers.CharField()
    date = serializers.DateField()
    warehouse_action_id = serializers.IntegerField()
    onec_ttn_id = serializers.IntegerField(required=False, allow_null=True, default=None)
