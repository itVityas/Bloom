from rest_framework import serializers

from apps.sez.models import InnerTTNItems
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class InnerTTNItemsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerTTNItems
        fields = "__all__"

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError('Количество не может быть меньше 0')
        if InnerTTNItems.objects.filter(inner_ttn=data['inner_ttn'], model_name=data['model_name']).exists():
            raise serializers.ValidationError('Товар в накладной уже существует')
        return data


class InnerTTNItemsSerializer(serializers.ModelSerializer):
    model_name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = InnerTTNItems
        fields = "__all__"
