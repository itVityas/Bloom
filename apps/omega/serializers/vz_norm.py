from rest_framework import serializers
from apps.omega.models import VzNorm

class VzNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = VzNorm
        fields = '__all__'
