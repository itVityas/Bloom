from rest_framework import serializers


class ConsignmentSerializer(serializers.Serializer):
    """
    Serializer for consignment data with comprehensive validation.

    Handles serialization and validation of consignment information including:
    - Document identification
    - Recipient details
    - Quantity and article information
    - Invoice references
    - Tax and product identifiers

    All fields include proper validation and documentation for API consumers.
    """
    document_number = serializers.CharField(max_length=20)
    doc_date = serializers.IntegerField()
    recipient = serializers.CharField(max_length=250, required=False,
                                      allow_blank=True, allow_null=True)
    recipient_code = serializers.CharField(max_length=7, required=False,
                                           allow_blank=True, allow_null=True)
    quantity = serializers.FloatField()
    article = serializers.CharField(max_length=25, required=False,
                                    allow_blank=True, allow_null=True)
    invoice_number = serializers.CharField(
        max_length=20, required=False, allow_blank=True, allow_null=True)
    invoice_series = serializers.CharField(
        max_length=4, required=False, allow_blank=True, allow_null=True)
    unp = serializers.CharField(max_length=20)
    gtin = serializers.CharField(max_length=14, required=False,
                                 allow_blank=True, allow_null=True)
