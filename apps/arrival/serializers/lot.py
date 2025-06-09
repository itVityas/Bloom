from rest_framework import serializers

from apps.arrival.models import Lot


class LotPostSerializer(serializers.ModelSerializer):
    """
    Serializer for Lot model.
    """
    class Meta:
        model = Lot
        fields = '__all__'


class LotGetSerializer(serializers.ModelSerializer):
    """
    Serializer for Lot model.
    """
    class Meta:
        model = Lot
        fields = '__all__'
