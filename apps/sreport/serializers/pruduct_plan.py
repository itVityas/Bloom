from rest_framework import serializers

from apps.sreport.models import ProductPlan
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.serializers.workplaces import WorkplacesSerializer


class ProductPlanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPlan
        fields = '__all__'


class ProductPlanGetSerializer(serializers.ModelSerializer):
    module = ModulesSerializer()
    workplace = WorkplacesSerializer()

    class Meta:
        model = ProductPlan
        fields = '__all__'
