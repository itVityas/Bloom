from rest_framework import serializers

from apps.warehouse.models import WarehouseTTN
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import WarehouseActionGetSerializer
from apps.account.serializers.user import UserSerializer


class WarehouseTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTTN
        fields = [
            'ttn_number',
            'is_close',
            'date',
            'warehouse',
            'warehouse_action',
            'pallet',
        ]


class WarehouseTTNGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseTTN
        fields = '__all__'
