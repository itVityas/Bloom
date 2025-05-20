from rest_framework import serializers

from apps.shtrih.models import ModelNames


class ModelNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelNames
        fields = '__all__'


class CountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    code = serializers.IntegerField()
