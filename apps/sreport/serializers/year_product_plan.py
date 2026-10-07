from rest_framework import serializers

from apps.sreport.models import YearProductPlan


class YearProductPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearProductPlan
        fields = '__all__'
