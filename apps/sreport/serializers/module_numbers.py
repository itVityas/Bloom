from rest_framework import serializers


class ModuleNumbersSerializer(serializers.Serializer):
    is_segregation_needed = serializers.BooleanField(write_only=True, default=False)
    is_other_production_module_needed = serializers.BooleanField(write_only=True, default=False)
