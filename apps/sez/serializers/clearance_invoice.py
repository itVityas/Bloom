from rest_framework import serializers

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.sez.serializers.clearance_invoice_items import ClearanceInvoiceItemsFullSerializer
from apps.arrival.serializers.order import OrderSerializer


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
    order = OrderSerializer(read_only=True)

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
            'date_payments',
            'date_calc',
            'order',
            'is_gifted',
            'only_panel',
            'items',
        ]

    def get_items(self, obj) -> dict:
        """
        Returns the nested ClearanceInvoiceItems for the given ClearanceInvoice.
        """
        items = ClearanceInvoiceItems.objects.filter(clearance_invoice=obj)
        serializer = ClearanceInvoiceItemsFullSerializer(items, many=True)
        return serializer.data
