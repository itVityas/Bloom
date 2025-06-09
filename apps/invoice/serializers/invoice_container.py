from rest_framework import serializers

from apps.invoice.models import InvoiceContainer, TrainDoc
from apps.arrival.models import Container, Order
from apps.invoice.utils.check_excel import find_sheet


class OrderSmallSerializer(serializers.ModelSerializer):
    """Serializer for Container model"""
    class Meta:
        model = Order
        fields = '__all__'


class ContainerSmallSerializer(serializers.ModelSerializer):
    """Serializer for Container model."""
    order = OrderSmallSerializer(read_only=True)

    class Meta:
        model = Container
        fields = '__all__'


class InvoiceContainerPostSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceContainer model."""
    class Meta:
        model = InvoiceContainer
        fields = [
            'number',
            'date',
            'container'
        ]

    def create(self, validated_data):
        validated_data['sheet'] = self._fill_sheet(
            validated_data['number'],
            validated_data['container']
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        number = validated_data.get('number', instance.number)
        container = validated_data.get('container', instance.container)
        validated_data['sheet'] = self._fill_sheet(
            number,
            container
        )
        return super().update(instance, validated_data)

    def _fill_sheet(self, number, container) -> str:
        """Fill sheet with data from instance."""
        container_name = container.name
        invoice = TrainDoc.objects.filter(lot=container.lot).first()
        if not invoice:
            return None
        file = invoice.file
        return find_sheet(invoice_number=number, container_name=container_name, file=file)
        return None


class InvoiceContainerGetSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceContainer model."""
    container = ContainerSmallSerializer(read_only=True)

    class Meta:
        model = InvoiceContainer
        fields = '__all__'
