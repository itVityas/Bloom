from rest_framework import serializers

from apps.arrival.models import Order, Container
from apps.arrival.serializers.container import ContainerFullSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    containers = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'containers',
        ]

    def get_containers(self, obj) -> dict:
        containers = Container.objects.filter(order=obj)
        return ContainerFullSerializer(containers, many=True).data
