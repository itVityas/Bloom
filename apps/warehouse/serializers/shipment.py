from rest_framework import serializers

from apps.warehouse.models import Shipment
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_products import WarehouseProductGetSerializer
from apps.onec.serializers.onec_ttn import OneCTTNFullSerializer
from apps.account.serializers.user import UserSerializer


class ShipmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'warehouse',
            'warehouse_product',
            'onec_ttn',
            'user',
            'quantity',
        ]


class ShipmentGetSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_product = WarehouseProductGetSerializer(read_only=True)
    onec_ttn = OneCTTNFullSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
