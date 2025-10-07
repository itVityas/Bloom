from rest_framework import serializers


class DataForMainDocSerializer(serializers.Serializer):
    from_date = serializers.DateField(write_only=True, required=False, default=None)
    to_date = serializers.DateField(write_only=True, required=False, default=None)
    model = serializers.CharField(write_only=True, required=False, default=None)
    module = serializers.IntegerField(write_only=True, required=False, default=None)
    shift = serializers.CharField(write_only=True, required=False, default=None)
    is_period = serializers.BooleanField(write_only=True, default=False)
    is_month = serializers.BooleanField(write_only=True, default=False)
    is_other_production = serializers.BooleanField(write_only=True, default=False)
    group = serializers.CharField(write_only=True, required=False, default=None)
    ordering = serializers.CharField(write_only=True, required=False, default=None)


class DataForMainDocResponseSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    variant_code = serializers.CharField()
    module = serializers.IntegerField()
    designation = serializers.CharField()   # Обозначение letter_part + numeric_part + execution_part
    assembly = serializers.IntegerField()
    extract = serializers.IntegerField()
    packaging = serializers.IntegerField()
    shift = serializers.CharField()
