from rest_framework import serializers


class ClearItemsRequestSerializer(serializers.Serializer):
    order_number = serializers.IntegerField()
    model = serializers.CharField()
    quantity = serializers.IntegerField()
    is_tv = serializers.BooleanField(required=False)
