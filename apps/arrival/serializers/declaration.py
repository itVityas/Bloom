from rest_framework import serializers
from apps.arrival.models import Declaration
from apps.arrival.serializers.declared_item import DeclaredItemSerializer


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all__'


class DeclarationFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class DeclarationAndItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Declaration
        fields = '__all__'

    declared_items = DeclaredItemSerializer(many=True, read_only=True)


class DeclarationAndItemFileUploadSerializer(serializers.Serializer):
    decl_file = serializers.FileField()
    tovar_file = serializers.FileField()
    container_id = serializers.IntegerField()
