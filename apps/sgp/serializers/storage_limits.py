from rest_framework import serializers

from apps.sgp.models import StorageLimits


class StorageLimitsGetSerializer(serializers.ModelSerializer):
    """
    Serializer for the StorageLimits model for get api
    """
    class Meta:
        model = StorageLimits
        fields = '__all__'


class StorageLimitsPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the StorageLimits model for post api
    """
    class Meta:
        model = StorageLimits
        fields = '__all__'
