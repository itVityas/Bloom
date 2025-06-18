import os

from rest_framework import serializers

from apps.invoice.models import TrainDoc, InvoiceContainer
from apps.arrival.models import Container
from apps.invoice.utils.check_excel import find_sheet
from apps.invoice.utils.sheet_count import sheet_count


class TrainDocPostSerializer(serializers.ModelSerializer):
    """Serializer for create and update TrainDoc model."""
    class Meta:
        model = TrainDoc
        fields = [
            'lot',
            'file'
        ]

    def create(self, validated_data):
        return self._check_save(validated_data)

    def update(self, instance, validated_data):
        file = validated_data.get('file', instance.file)
        lot = validated_data.get('lot', instance.lot)
        containers = Container.objects.filter(lot=lot)
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
        """Check save TrainDoc model."""
        inst_file = None
        inst_lot = None
        if instance:
            inst_file = instance.file
            inst_lot = instance.lot
        file = validated_date.get('file', inst_file)
        lot = validated_date.get('lot', inst_lot)
        if not file or not lot:
            raise serializers.ValidationError('File and order are required')

        invoice = TrainDoc.objects.filter(lot=lot).first()
        if invoice:
            if not os.path.exists(invoice.file.path):
                invoice.prev_file = None
            else:
                invoice.prev_file = invoice.file
            invoice.file = file
            invoice.filename = file.name
            invoice.sheet_count = sheet_count(file)
            invoice.save()
            return invoice
        if instance:
            if not os.path.exists(invoice.file.path):
                invoice.prev_file = None
            else:
                invoice.prev_file = invoice.file
            instance.file = file
            invoice.filename = file.name
            invoice.sheet_count = sheet_count(file)
            instance.save()
            return instance
        count = sheet_count(file)
        return TrainDoc.objects.create(lot=lot, file=file, filename=file.name, sheet_count=count)


class TrainDocGetSerializer(serializers.ModelSerializer):
    """Serializer for get TrainDoc model."""
    class Meta:
        model = TrainDoc
        fields = '__all__'
