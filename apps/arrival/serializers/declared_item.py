from rest_framework import serializers
from apps.arrival.models import DeclaredItem


class DeclaredItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaredItem
        fields = '__all__'


class DeclaredItemFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()