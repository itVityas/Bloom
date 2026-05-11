from rest_framework import serializers

from apps.sreport.models import WarehouseTTNBarcode


class WarehouseTTNBarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTTNBarcode
        fields = '__all__'
