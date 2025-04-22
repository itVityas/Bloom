from rest_framework import serializers

from apps.shtrih.models import Products
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.serializers.model import ModelsSerializer


class ProductGetSerializer(serializers.ModelSerializer):
    color_id = ColorsSerializer(read_only=True)
    model = ModelsSerializer(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'
