from rest_framework import serializers

from apps.invoice.models import InvoiceContainer


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
    class Meta:
        model = InvoiceContainer
        fields = '__all__'
