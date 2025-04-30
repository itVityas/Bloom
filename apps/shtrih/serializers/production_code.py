from rest_framework import serializers

from apps.shtrih.models import Production_codes


class ProductionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production_codes
        fields = '__all__'
