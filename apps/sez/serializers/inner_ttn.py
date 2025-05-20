from rest_framework import serializers

from apps.sez.models import InnerTTN, InnerTTNItems
from apps.sez.serializers.inner_ttn_item import InnerTTNItemsSerializer
from django.db.models import Sum


class InnerTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerTTN
        fields = "__all__"


class InnerTTNSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    full_price = serializers.SerializerMethodField()
    full_quantity = serializers.SerializerMethodField()

    class Meta:
        model = InnerTTN
        fields = "__all__"

    def get_items(self, obj) -> dict:
        items = InnerTTNItems.objects.filter(inner_ttn=obj)
        return InnerTTNItemsSerializer(items, many=True).data

    def get_full_price(self, obj) -> float:
        price = InnerTTNItems.objects.filter(inner_ttn=obj).aggregate(
            full_price=Sum("price_pcs")
        )
        return price.get('full_price', 0)

    def get_full_quantity(self, obj) -> int:
        quantity = InnerTTNItems.objects.filter(inner_ttn=obj).aggregate(
            full_quantity=Sum("quantity")
        )
        return quantity.get('full_quantity', 0)
