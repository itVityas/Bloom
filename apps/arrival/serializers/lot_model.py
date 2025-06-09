from rest_framework import serializers

from apps.arrival.models import LotModel


class LotModelPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotModel
        fields = '__all__'
