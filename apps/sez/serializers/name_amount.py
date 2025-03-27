from rest_framework import serializers


class NameAmountSerializer(serializers.Serializer):
    name__id = serializers.IntegerField()
    name__short_name = serializers.CharField()
    code = serializers.IntegerField()
    real_amount = serializers.IntegerField()
