from rest_framework import serializers

from apps.sreport.models import WarehouseMonthModelCount


class WarehouseModelMonthCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseMonthModelCount
        fields = '__all__'
