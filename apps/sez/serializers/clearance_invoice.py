from rest_framework import serializers

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.sez.serializers.clearance_invoice_items import ClearanceInvoiceItemsFullSerializer
from apps.arrival.serializers.order import OrderSerializer
from apps.account.serializers.user import UserSerializer
from apps.sez.exceptions import TTNUsedException


class ClearanceInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    class Meta:
        model = ClearanceInvoice
        fields = '__all__'

    def validate(self, attrs):
        clearance_invoice = ClearanceInvoice.objects.filter(ttn=attrs.get('ttn'))
        if clearance_invoice:
            raise TTNUsedException(ttn_name=attrs.get('ttn'), invoice_id=clearance_invoice.first().id)
        return super().validate(attrs)


class FullClearanceInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model with nested ClearanceInvoiceItems.
    """
    items = serializers.SerializerMethodField()
    order = OrderSerializer(read_only=True, many=True)
    responsible = UserSerializer(read_only=True)

    class Meta:
        model = ClearanceInvoice
        fields = [
            'id',
            'count',
            'cleared',
            'ttn',
            'recipient',
            'create_at',
            'date_payments',
            'date_calc',
            'order',
            'is_gifted',
            'only_panel',
            'items',
            'responsible',
        ]

    def get_items(self, obj) -> dict:
        """
        Returns the nested ClearanceInvoiceItems for the given ClearanceInvoice.
        """
        items = ClearanceInvoiceItems.objects.filter(clearance_invoice=obj)
        serializer = ClearanceInvoiceItemsFullSerializer(items, many=True)
        return serializer.data
