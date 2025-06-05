from rest_framework import serializers

from apps.invoice.models import InvoiceContainer
from apps.arrival.models import Container, Order


class OrderSmallSerializer(serializers.ModelSerializer):
    """Serializer for Container model"""
    class Meta:
        model = Order
        fields = '__all__'


class ContainerSmallSerializer(serializers.ModelSerializer):
    """Serializer for Container model."""
    order = OrderSmallSerializer(read_only=True)

    class Meta:
        model = Container
        fields = '__all__'


class InvoiceContainerPostSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceContainer model."""
    class Meta:
        model = InvoiceContainer
        fields = [
            'number',
            'date',
            'container'
        ]


class InvoiceContainerGetSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceContainer model."""
    container = ContainerSmallSerializer(read_only=True)

    class Meta:
        model = InvoiceContainer
        fields = '__all__'
