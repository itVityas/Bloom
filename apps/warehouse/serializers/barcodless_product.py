from rest_framework import serializers

from apps.warehouse.models import BarcodlessProducts
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class BarcodlessProductSerializer(serializers.ModelSerializer):
    """ Serializer for BarcodlessProduct without linked models"""
    class Meta:
        model = BarcodlessProducts
        fields = "__all__"


class BarcodlessProductFullSerializer(serializers.ModelSerializer):
    """ Serializer for BarcodlessProduct with linked models"""
    model_name = ModelNamesSerializer()
    color = ColorsSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = BarcodlessProducts
        fields = "__all__"
