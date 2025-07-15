from rest_framework import serializers

from apps.warehouse.models import WarehouseTTN


class WarehouseTTNSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTTN
        fields = '__all__'
