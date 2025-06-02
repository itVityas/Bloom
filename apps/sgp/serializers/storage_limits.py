from rest_framework import serializers

from apps.sgp.models import StorageLimits


class StorageLimitsGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving StorageLimits records with detailed information.

    Provides complete storage limit information including:
    - Maximum storage days
    - Production code reference
    - Optional model-specific code

    This serializer is read-only and used for GET operations.
    """
    class Meta:
        model = StorageLimits
        fields = '__all__'


class StorageLimitsPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating StorageLimits records.

    Handles validation for:
    - Storage day limits (1-365 days)
    - Production code requirements
    - Business logic constraints
    """
    class Meta:
        model = StorageLimits
        fields = '__all__'
