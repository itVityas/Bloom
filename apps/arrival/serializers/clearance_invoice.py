from rest_framework import serializers
from apps.arrival.models import ClearanceInvoice

class ClearanceInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoice model.
    """
    class Meta:
        model = ClearanceInvoice
        fields = '__all__'