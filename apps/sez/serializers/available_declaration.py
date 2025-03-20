from rest_framework import serializers


class AvailableDeclarationSerializer(serializers.Serializer):
    declaration__id = serializers.IntegerField()
    declaration__declaration_number = serializers.CharField()
    ordinal_number = serializers.IntegerField()
    real_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit_name = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
