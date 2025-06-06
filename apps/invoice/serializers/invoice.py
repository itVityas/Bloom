from rest_framework import serializers

from apps.invoice.models import Invoice, InvoiceContainer
from apps.arrival.models import Container
from apps.invoice.utils.check_excel import find_sheet


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
        file = validated_data.get('file', instance.file)
        order = validated_data.get('order', instance.order)
        containers = Container.objects.filter(order=order)
        for container in containers:
            container_invoices = InvoiceContainer.objects.filter(container=container)
            for container_invoice in container_invoices:
                container_invoice.sheet = find_sheet(
                    container_name=container.name,
                    invoice_number=container_invoice.number,
                    file=file)
                container_invoice.save()
        return self._check_save(validated_data, instance)

    def _check_save(self, validated_date, instance=None):
        """Check save Invoice model."""
        inst_file = None
        inst_order = None
        if instance:
            inst_file = instance.file
            inst_order = instance.order
        file = validated_date.get('file', inst_file)
        order = validated_date.get('order', inst_order)
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
