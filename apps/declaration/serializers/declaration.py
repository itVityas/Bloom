from rest_framework import serializers

from apps.arrival.models import Order, Container
from apps.declaration.models import Declaration
from apps.declaration.serializers.declared_item import DeclaredItemSerializer


class DeclarationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Declaration model.
    """
    containers = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Declaration
        fields = '__all__'

    def get_containers(self, obj) -> dict:
        """
        Get the container IDs associated with the declaration.
        """
        if obj.container is None:
            return None
        containers = obj.container
        return ContainerSmallSerializer(containers).data

    def get_orders(self, obj) -> dict:
        """
        Get the order IDs associated with the declaration.
        """
        if obj.container is None:
            return None
        if obj.container.order is None:
            return None
        orders = obj.container.order
        return OrderSmallSerializer(orders).data


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


class ContainerSmallSerializer(serializers.ModelSerializer):
    """
    Serializer for Container model with id and name
    """
    class Meta:
        model = Container
        fields = ('id', 'name')


class OrderSmallSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model with id and name
    """
    class Meta:
        model = Order
        fields = ('id', 'name')
