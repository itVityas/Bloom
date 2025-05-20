from rest_framework import serializers

from apps.sez.models import InnerTTNItems
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class InnerTTNItemsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerTTNItems
        fields = "__all__"


class InnerTTNItemsSerializer(serializers.ModelSerializer):
    model_name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = InnerTTNItems
        fields = "__all__"
