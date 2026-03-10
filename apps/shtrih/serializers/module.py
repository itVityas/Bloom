from rest_framework import serializers

from apps.shtrih.models import Modules, Workplaces


class ModulesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Modules model representing product components/modules.

    Handles serialization and deserialization of module data including:
    - Module identification numbers
    - Digit codes

    Fields:
        - id: Auto-generated primary key
        - number: Module identification number
        - digit: Module classification digit
    """
    class Meta:
        model = Modules
        fields = '__all__'


class WorkplacesLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplaces
        fields = '__all__'


class ModulesWorkplacesSerializer(serializers.ModelSerializer):
    workplaces_set = WorkplacesLightSerializer(many=True, read_only=True)

    class Meta:
        model = Modules
        fields = ('id', 'number', 'digit', 'workplaces_set')
