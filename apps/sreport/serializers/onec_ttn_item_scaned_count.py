from rest_framework import serializers

from apps.sreport.models import OneCTTNItemScanedCount


class OneCTTNItemScanedCountGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTNItemScanedCount
        fields = '__all__'
