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

        model_name = data.get('model_name')
        inner_ttn = data.get('inner_ttn')
        if not model_name:
            model_name = self.instance.model_name
        if not inner_ttn:
            inner_ttn = self.instance.inner_ttn
        item_id = None
        if self.instance:
            item_id = self.instance.id
        if InnerTTNItems.objects.exclude(id=item_id).filter(inner_ttn=inner_ttn, model_name=model_name).exists():
            raise serializers.ValidationError('Товар в накладной уже существует')
        return data


class InnerTTNItemsSerializer(serializers.ModelSerializer):
    model_name = ModelNamesSerializer(read_only=True)

    class Meta:
        model = InnerTTNItems
        fields = "__all__"
