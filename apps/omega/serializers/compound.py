from rest_framework import serializers


class analogSerializer(serializers.Serializer):
    item_sign = serializers.CharField()
    koef = serializers.DecimalField(max_digits=19, decimal_places=4)
    name = serializers.CharField()
    nomsign = serializers.CharField()


class CompoundSerializer(serializers.Serializer):
    item_sign = serializers.CharField()
    item_unv = serializers.CharField()
    nomsign = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=19, decimal_places=4)
    analogs = analogSerializer(many=True)
