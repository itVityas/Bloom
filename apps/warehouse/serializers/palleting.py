from rest_framework import serializers

from apps.warehouse.models import Palleting
from apps.warehouse.serializers.pallet import PalletSerializer
from apps.warehouse.serializers.warehouse_products import (
    WarehouseProductGetSerializer
)
from apps.account.serializers.user import UserUpdateSerializer


class PalletingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palleting
        fields = [
            'pallet',
            'warehouse_product',
        ]


class PalletingGetSerializer(serializers.ModelSerializer):
    pallet = PalletSerializer(read_only=True, many=False)
    warehouse_product = WarehouseProductGetSerializer(
        read_only=True, many=False)
    user = UserUpdateSerializer(read_only=True, many=False)

    class Meta:
        model = Palleting
        fields = "__all__"
