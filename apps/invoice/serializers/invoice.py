from rest_framework import serializers

from apps.invoice.models import Invoice


class InvoicePostSerializer(serializers.ModelSerializer):
    """Serializer for create and update Invoice model."""
    class Meta:
        model = Invoice
        fields = [
            'order',
            'file'
        ]

    def create(self, validated_data):
        return self._check_save(validated_data)

    def update(self, instance, validated_data):
        return self._check_save(validated_data, instance)

    def _check_save(self, validated_date, instance=None):
        file = validated_date.get('file', None)
        order = validated_date.get('order', None)
        if not file or not order:
            raise serializers.ValidationError('File and order are required')

        invoice = Invoice.objects.filter(order=order).first()
        if invoice:
            invoice.prev_file = invoice.file
            invoice.file = file
            invoice.filename = file.name
            invoice.save()
            return invoice
        if instance:
            instance.prev_file = instance.file
            instance.file = file
            invoice.filename = file.name
            instance.save()
            return instance
        return Invoice.objects.create(order=order, file=file, filename=file.name)


class InvoiceGetSerializer(serializers.ModelSerializer):
    """Serializer for get Invoice model."""
    class Meta:
        model = Invoice
        fields = '__all__'
