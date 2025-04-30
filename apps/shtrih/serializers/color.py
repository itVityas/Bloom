from rest_framework import serializers

from apps.shtrih.models import Colors


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'
