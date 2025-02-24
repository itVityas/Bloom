from rest_framework import serializers
from apps.arrival.models import Declaration
from apps.arrival.serializers.declared_item import DeclaredItemSerializer


class DeclarationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Declaration model.
    """
    class Meta:
        model = Declaration
        fields = '__all__'


class DeclarationFileUploadSerializer(serializers.Serializer):
    """
    Serializer for file upload to create Declarations.
    """
    file = serializers.FileField()


class DeclarationAndItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Declaration with related DeclaredItems.
    """
    declared_items = DeclaredItemSerializer(many=True, read_only=True)

    class Meta:
        model = Declaration
        fields = '__all__'


class DeclarationAndItemFileUploadSerializer(serializers.Serializer):
    """
    Serializer for file upload to create Declarations and DeclaredItems.
    """
    decl_file = serializers.FileField()
    tovar_file = serializers.FileField()
    container_id = serializers.IntegerField()


class DeclarationBindSerializer(serializers.Serializer):
    """
    Serializer for binding declarations to a container.

    If 'container_id' is null, declarations will be unbound (container set to None).
    """
    container_id = serializers.IntegerField(required=False, allow_null=True)
    declaration_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
