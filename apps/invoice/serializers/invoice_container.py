from rest_framework import serializers

from apps.invoice.models import InvoiceContainer


class InvoiceContainerPostSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceContainer model."""
    def create(self, validated_data):
        return InvoiceContainer.objects.create(**validated_data)

    class Meta:
        model = InvoiceContainer
        fields = '__all__'
