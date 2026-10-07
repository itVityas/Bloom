from rest_framework import serializers

from apps.sreport.models import MonthProductPlan


class MonthProductPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthProductPlan
        fields = '__all__'
