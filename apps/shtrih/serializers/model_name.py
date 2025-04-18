from rest_framework import serializers

from apps.shtrih.models import ModelNames


class ModelNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelNames
        fields = '__all__'
