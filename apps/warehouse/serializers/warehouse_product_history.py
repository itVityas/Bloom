from rest_framework import serializers

from apps.warehouse.models import WarehouseProductHistory
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import (
    WarehouseActionGetSerializer)
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.account.serializers.user import UserUpdateSerializer


class WarehouseProductHistoryGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)
    user = UserUpdateSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseProductHistory
        fields = '__all__'
