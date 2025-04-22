from rest_framework import serializers

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.declaration.models import DeclaredItem
from apps.sez.serializers.clearance_invoice_items import ClearanceInvoiceItemsFullSerializer
from apps.declaration.serializers.declared_item import DeclaredItemSerializer


class ClearanceInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    class Meta:
        model = ClearanceInvoice
        fields = '__all__'


class FullClearanceInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model with nested ClearanceInvoiceItems.
    """
    items = serializers.SerializerMethodField()

    class Meta:
        model = ClearanceInvoice
        fields = [
            'id',
            'count',
            'cleared',
            'ttn',
            'series',
            'recipient',
            'quantity_shipped',
            'create_at',
            'date_cleared',
            'date_payments',
            'date_calc',
            'items',
        ]

    def get_items(self, obj) -> dict:
        """
        Returns the nested ClearanceInvoiceItems for the given ClearanceInvoice.
        """
        items = ClearanceInvoiceItems.objects.filter(clearance_invoice=obj)
        serializer = ClearanceInvoiceItemsFullSerializer(items, many=True)
        return serializer.data
