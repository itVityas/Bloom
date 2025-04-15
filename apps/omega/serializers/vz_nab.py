from rest_framework import serializers
from apps.omega.models import VzNab


class VzNabSerializer(serializers.ModelSerializer):
    class Meta:
        model = VzNab
        fields = '__all__'
