from rest_framework import serializers
from apps.arrival.models import Order, Container
from apps.arrival.serializers.container import ContainerFullSerializer, ContainerAndDeclarationSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with their associated containers.
    """
    containers = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'containers',
        ]

    def get_containers(self, obj) -> list:
        """
        Returns serialized containers associated with the given order.

        :param obj: Order instance.
        :return: List of serialized container data.
        """
        # It is assumed that Container model has a ForeignKey to Order.
        containers = Container.objects.filter(order=obj)
        return ContainerFullSerializer(containers, many=True).data


class OrderWithContainerSerializer(serializers.ModelSerializer):
    """
    Serializer for Order with its associated containers (with declarations).
    """
    containers = ContainerAndDeclarationSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
