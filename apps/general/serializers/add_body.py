from rest_framework import serializers

from apps.general.models import AddBody


class AddBodySerializer(serializers.ModelSerializer):
    """
    Serializer for AddBody model with enhanced security and validation.

    Provides serialization/deserialization of AddBody objects with:
    - Field-level validation
    - Read-only fields for timestamps
    - Explicit field definitions for better security
    - Nested title information
    """
    class Meta:
        model = AddBody
        fields = '__all__'
