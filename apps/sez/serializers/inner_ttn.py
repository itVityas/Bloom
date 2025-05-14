from rest_framework import serializers

from apps.sez.models import InnerTTN, InnerTTNItems
from apps.sez.serializers.inner_ttn_item import InnerTTNItemsSerializer


class InnerTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerTTN
        fields = "__all__"


class InnerTTNSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = InnerTTN
        fields = "__all__"

    def get_items(self, obj) -> dict:
        items = InnerTTNItems.objects.filter(inner_ttn=obj)
        return InnerTTNItemsSerializer(items, many=True).data
