from django.utils import timezone
from rest_framework import serializers

from apps.warehouse.models import WarehouseProduct, WarehouseTTN
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.warehouse.serializers.warehouse_action import (
    WarehouseActionGetSerializer)
from apps.warehouse.serializers.warehouse_ttn import WarehouseTTNSerializer
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.account.serializers.user import UserUpdateSerializer
from apps.shtrih.models import Products


class WarehouseProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = [
            'product',
            'warehouse',
            'warehouse_action',
            'warehouse_ttn',
            'quantity',
            'ttn_number',
            'date'
        ]


class WarehouseProductGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionGetSerializer(read_only=True, many=False)
    user = UserUpdateSerializer(read_only=True, many=False)
    warehouse_ttn = WarehouseTTNSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseProduct
        fields = "__all__"


class WarehouseProductBarcodeSerializer(serializers.ModelSerializer):
    warehouse_ttn = serializers.CharField()
    barcode = serializers.CharField(write_only=True)

    class Meta:
        model = WarehouseProduct
        fields = [
            'barcode',
            'warehouse',
            'warehouse_action',
            'warehouse_ttn',
            'quantity',
            'ttn_number',
            'date'
        ]
        extra_kwargs = {
            'product': {'read_only': True},
            'user': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs.get('warehouse_ttn', None):
            if not WarehouseTTN.objects.filter(
                    ttn_number=attrs['warehouse_ttn']).exists():
                WarehouseTTN.objects.create(
                    ttn_number=attrs['warehouse_ttn'],
                    is_close=False,
                    date=timezone.now())
        return super().validate(attrs)

    def validate_barcode(self, value):
        if not Products.objects.filter(barcode=value).exists():
            raise serializers.ValidationError("Product with this barcode does not exist")
        return value

    def create(self, validated_data):
        barcode = validated_data.pop('barcode')
        product = Products.objects.get(barcode=barcode)

        if not validated_data.get('quantity', None):
            validated_data['quantity'] = product.quantity

        validated_data['user'] = self.context['request'].user
        validated_data['warehouse_ttn'] = WarehouseTTN.objects.get(
            ttn_number=validated_data['warehouse_ttn'])

        return WarehouseProduct.objects.create(
            product=product,
            **validated_data
        )
