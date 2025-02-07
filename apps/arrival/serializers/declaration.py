from rest_framework import serializers
from apps.arrival.models import Declaration


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all__'


class DeclarationFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
