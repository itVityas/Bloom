from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ListOrderSerializer(serializers.Serializer):
    orders_id = OrderItemSerializer(
        many=True,
        help_text="List of orders")
