from rest_framework import serializers


class NameAmountSerializer(serializers.Serializer):
    name__id = serializers.IntegerField()
    name__short_name = serializers.SerializerMethodField()
    name__name = serializers.CharField()
    code = serializers.IntegerField()
    real_amount = serializers.IntegerField()

    def get_name__short_name(self, obj) -> str:
        if obj.get('name__short_name', None) is None:
            return obj.get('name__name', None)
        return obj.get('name__short_name', None)
