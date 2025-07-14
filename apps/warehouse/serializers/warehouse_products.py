from rest_framework import serializers

from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import (
    WarehouseActionGetSerializer)
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.account.serializers.user import UserUpdateSerializer


class WarehouseProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = [
            'product',
            'warehouse',
            'warehouse_action',
            'quantity',
            'ttn_number'
        ]


class WarehouseProductGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)
    user = UserUpdateSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseProduct
        fields = "__all__"
