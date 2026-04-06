from django.db import transaction

from rest_framework import serializers

from apps.onec.models import OneCTTN, OneCTTNItem
from apps.shtrih.models import Models
from apps.onec.serializers.onec_ttn_item import (
    OneCTTNItemListSerializer, OneCTTNItemDesinerSerializer)


class OneCTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTN
        fields = "__all__"


class OneCTTNGetSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = OneCTTN
        fields = "__all__"

    def get_items(self, obj) -> dict:
        items = OneCTTNItem.objects.filter(onec_ttn=obj)
        return OneCTTNItemListSerializer(items, many=True).data


class OneCTTNFullSerializer(serializers.ModelSerializer):
    items = OneCTTNItemDesinerSerializer(many=True, write_only=True)

    class Meta:
        model = OneCTTN
        fields = [
            'number',
            'series',
            'items',
        ]

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('items', None)
            number = validated_data.get('number', None)
            series = validated_data.get('series', None)
            if OneCTTN.objects.filter(number=number, series=series).exists():
                raise serializers.ValidationError('TTN already exists')
            OneCTTN.objects.create(**validated_data)
            ttn = OneCTTN.objects.filter(**validated_data).first()

            for item in items_data:
                count = item.get('count', None)
                desiner_code = item.get('desiner_code', None)
                name = item.get('name', None)
                model = None
                if desiner_code:
                    model = Models.objects.filter(design_code=desiner_code).first()
                if not model:
                    model = Models.objects.filter(name=name).first()
                if not count or not model:
                    raise serializers.ValidationError('no model or count')
                OneCTTNItem.objects.create(onec_ttn=ttn, count=count, model_name=model.name)

        return ttn
