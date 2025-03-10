from rest_framework import serializers

from apps.invoice.models import InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the InvoiceItem model.
    This serializer includes all fields of the InvoiceItem model without nested data.
    """
    class Meta:
        model = InvoiceItem
        fields = '__all__'
