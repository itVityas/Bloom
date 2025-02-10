from rest_framework import serializers


class ConsignmentSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=20)
    doc_date = serializers.DateField()
    recipient = serializers.CharField(max_length=250)
    recipient_code = serializers.CharField(max_length=7)
    quantity = serializers.IntegerField()
    article = serializers.CharField(max_length=25)
    invoice_number = serializers.CharField(max_length=20)
    invoice_series = serializers.CharField(max_length=4)
    unp = serializers.CharField(max_length=20)
    gtin = serializers.CharField(max_length=14)
