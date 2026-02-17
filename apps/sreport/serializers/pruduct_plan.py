from rest_framework import serializers

from apps.sreport.models import ProductPlan
from apps.shtrih.serializers.module import ModulesSerializer


class ProductPlanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPlan
        fields = '__all__'


class ProductPlanGetSerializer(serializers.ModelSerializer):
    module = ModulesSerializer()

    class Meta:
        model = ProductPlan
        fields = '__all__'
