from rest_framework import serializers

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.onec.serializers.onec_ttn_item import (
    OneCTTNItemSerializer, OneCTTNItemListSerializer)


class OneCTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTN
        fields = "__all__"


class OneCTTNGetSerializer(serializers.ModelSerializer):
    items = OneCTTNItemSerializer(many=True, read_only=True)

    class Meta:
        model = OneCTTN
        fields = "__all__"


class OneCTTNFullSerializer(serializers.ModelSerializer):
    items = OneCTTNItemListSerializer(many=True, write_only=True)

    class Meta:
        model = OneCTTN
        fields = [
            'number',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', None)
        ttn = OneCTTN.objects.create(**validated_data)

        for item in items_data:
            OneCTTNItem.objects.create(onec_ttn=ttn, **item)

        return ttn
