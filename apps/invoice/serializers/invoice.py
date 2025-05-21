from rest_framework import serializers

from apps.invoice.models import Invoice, InvoiceItem
from apps.invoice.serializers.invoice_item import InvoiceItemSerializer
from apps.arrival.serializers.container import ContainerAndOrderSerializer


class InvoiceFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model with nested InvoiceItem data.
    This serializer includes all fields of the Invoice model and a custom field 'items'
    that contains the serialized data of related InvoiceItem objects.
    """
    items = serializers.SerializerMethodField()
    container = ContainerAndOrderSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

    def get_items(self, obj) -> dict:
        """
        Method to retrieve and serialize related InvoiceItem objects.
        :param obj: The Invoice instance being serialized.
        :return: Serialized data of related InvoiceItem objects.
        """
        items = InvoiceItem.objects.filter(invoice=obj)
        return InvoiceItemSerializer(items, many=True).data


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the Invoice model.
    This serializer includes all fields of the Invoice model without nested data.
    """
    class Meta:
        model = Invoice
        fields = '__all__'
