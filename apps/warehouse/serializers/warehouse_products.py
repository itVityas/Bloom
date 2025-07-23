from rest_framework import serializers

from apps.warehouse.models import WarehouseProduct
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.account.serializers.user import UserUpdateSerializer
from apps.shtrih.models import Products, Protocols
from apps.warehouse.exceptions.barcode import (
    ProductNotFound, PaсkagingNotFound)
from apps.onec.serializers.onec_ttn import OneCTTNGetSerializer


class WarehouseProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = [
            'product',
            'quantity',
            'onec_ttn',
        ]


class WarehouseProductGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(read_only=True, many=False)
    user = UserUpdateSerializer(read_only=True, many=False)
    onec_ttn = OneCTTNGetSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseProduct
        fields = "__all__"


class WarehouseProductBarcodeSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)
    check_packaging = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = WarehouseProduct
        fields = [
            'barcode',
            'quantity',
            'onec_ttn',
            'check_packaging',
        ]
        extra_kwargs = {
            'product': {'read_only': True},
            'user': {'read_only': True}
        }

    def validate_barcode(self, value):
        if not Products.objects.filter(barcode=value).exists():
            raise ProductNotFound()
        return value

    def create(self, validated_data):
        barcode = validated_data.pop('barcode')
        product = Products.objects.get(barcode=barcode)
        check_packaging = validated_data.pop('check_packaging', False)

        if product:
            if check_packaging:
                is_packaging = Protocols.objects.\
                    filter(product=product).\
                    filter(workplace__type_of_work=3).\
                    exists()
                if not is_packaging:
                    raise PaсkagingNotFound()
        else:
            ProductNotFound()

        if not validated_data.get('quantity', None):
            validated_data['quantity'] = product.quantity

        validated_data['user'] = self.context['request'].user

        return WarehouseProduct.objects.create(
            product=product,
            **validated_data
        )
