from rest_framework import serializers


class RelevantModelNumberSerializer(serializers.Serializer):
    is_other_production_models = serializers.BooleanField(write_only=True)
