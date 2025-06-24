from rest_framework import serializers
from apps.sez.models import ClearanceInvoice

class DBFZipSerializer(serializers.Serializer):
    clearance_invoice_id = serializers.IntegerField()

    def validate_clearance_invoice_id(self, value):
        if not ClearanceInvoice.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"ClearanceInvoice with id={value} does not exist."
            )
        return value
