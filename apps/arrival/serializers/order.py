from rest_framework import serializers

from apps.arrival.models import Order, Container
from apps.arrival.serializers.container import (
    ContainerFullSerializer,
    ContainerAndDeclarationSerializer)
from apps.invoice.models import Invoice
from apps.invoice.serializers.invoice import InvoiceGetSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if Order.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError('Order with this name already exists')
        return attrs


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with their associated containers.
    """
    containers = serializers.SerializerMethodField()
    invoicefile = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'containers',
            'invoice',
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

    def get_invoicefile(self, obj) -> dict:
        """
        Returns serialized invoices associated with the given order.

        :param obj: Order instance.
        :return: List of serialized invoice data.
        """
        # It is assumed that Invoice model has a ForeignKey to Order.
        invoices = Invoice.objects.filter(order=obj).first()
        if not invoices:
            return {}
        return InvoiceGetSerializer(invoices).data


class OrderWithContainerSerializer(serializers.ModelSerializer):
    """
    Serializer for Order with its associated containers (with declarations).
    """
    containers = ContainerAndDeclarationSerializer(many=True, read_only=True)
    invoicefile = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_invoicefile(self, obj) -> dict:
        """
        Returns serialized invoices associated with the given order.

        :param obj: Order instance.
        :return: List of serialized invoice data.
        """
        # It is assumed that Invoice model has a ForeignKey to Order.
        invoices = Invoice.objects.filter(order=obj).first()
        if not invoices:
            return {}
        return InvoiceGetSerializer(invoices).data
