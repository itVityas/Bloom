from rest_framework import serializers


class ConsignmentSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=20)
    doc_date = serializers.IntegerField()
    recipient = serializers.CharField(max_length=250)
    recipient_code = serializers.CharField(max_length=7)
    quantity = serializers.FloatField()
    article = serializers.CharField(max_length=25, required=False)
    invoice_number = serializers.CharField(max_length=20, required=False)
    invoice_series = serializers.CharField(max_length=4, required=False)
    unp = serializers.CharField(max_length=20)
    gtin = serializers.CharField(max_length=14, required=False)
