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
    workplaces = serializers.SerializerMethodField('get_workplaces')

    class Meta:
        model = Modules
        fields = ('id', 'number', 'digit', 'workplaces')

    def get_workplaces(self, obj):
        workplaces = Workplaces.objects.filter(module=obj)
        request = self.context.get('request')
        if request:
            type_of_work_id = request.query_params.get('type_of_work_id')
            computer_number = request.query_params.get('computer_number')

            if type_of_work_id:
                workplaces = workplaces.filter(type_of_work_id=type_of_work_id)
            if computer_number:
                workplaces = workplaces.filter(computer_number__iexact=computer_number)

        return WorkplacesLightSerializer(workplaces, many=True).data
