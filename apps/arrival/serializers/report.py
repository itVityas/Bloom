from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class ListOrderSerializer(serializers.Serializer):
    list = OrderItemSerializer(
        many=True,
        help_text="List of orders")
