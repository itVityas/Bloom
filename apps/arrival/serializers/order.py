from rest_framework import serializers

from apps.arrival.models import Order, Container, Lot
from apps.arrival.serializers.container import (
    ContainerFullSerializer,
    ContainerAndDeclarationSerializer)
from apps.invoice.models import TrainDoc
from apps.invoice.serializers.traindoc import TrainDocGetSerializer
from apps.arrival.serializers.lot import LotPostSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if Order.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError('Заказ с таким именем уже существует')
        return attrs


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with their associated containers.
    """
    containers = serializers.SerializerMethodField()
    traindoc = serializers.SerializerMethodField()
    lots = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'containers',
            'traindoc',
            'lots',
        ]

    def get_containers(self, obj) -> list:
        """
        Returns serialized containers associated with the given order.

        :param obj: Order instance.
        :return: List of serialized container data.
        """
        # It is assumed that Container model has a ForeignKey to Order.
        containers = Container.objects.filter(order=obj)
        return ContainerFullSerializer(containers, many=True).data

    def get_lots(self, obj) -> list:
        """
        Returns serialized lots associated with the given order.

        :param obj: Order instance.
        :return: List of serialized lot data.
        """
        # It is assumed that Container model has a ForeignKey to Order.
        lots = Lot.objects.filter(order=obj)
        return LotPostSerializer(lots, many=True).data

    def get_traindoc(self, obj) -> dict:
        """
        Returns serialized invoices associated with the given order.

        :param obj: Order instance.
        :return: List of serialized invoice data.
        """
        # It is assumed that Invoice model has a ForeignKey to Order.
        invoices = TrainDoc.objects.filter(lot__order=obj).first()
        if not invoices:
            return {}
        return TrainDocGetSerializer(invoices).data


class OrderWithContainerSerializer(serializers.ModelSerializer):
    """
    Serializer for Order with its associated containers (with declarations).
    """
    containers = ContainerAndDeclarationSerializer(many=True, read_only=True)
    traindoc = serializers.SerializerMethodField()
    lots = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_traindoc(self, obj) -> dict:
        """
        Returns serialized invoices associated with the given order.

        :param obj: Order instance.
        :return: List of serialized invoice data.
        """
        # It is assumed that Invoice model has a ForeignKey to Order.
        invoices = TrainDoc.objects.filter(lot__order=obj).first()
        if not invoices:
            return {}
        return TrainDocGetSerializer(invoices).data

    def get_lots(self, obj) -> list:
        """
        Returns serialized lots associated with the given order.

        :param obj: Order instance.
        :return: List of serialized lot data.
        """
        # It is assumed that Container model has a ForeignKey to Order.
        lots = Lot.objects.filter(order=obj)
        return LotPostSerializer(lots, many=True).data
