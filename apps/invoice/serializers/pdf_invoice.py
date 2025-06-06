from rest_framework import serializers


class PDFInvoiceSerializer(serializers.Serializer):
    invoice_container_id = serializers.IntegerField()
