from rest_framework import serializers

from apps.sgp.models import ShipmentBans


class ShipmentBansGetSerializer(serializers.ModelSerializer):
    """
    Serializer for get ShipmentBans model
    """
    class Meta:
        model = ShipmentBans
        fields = '__all__'


class ShipmentBansPostSerializer(serializers.ModelSerializer):
    """
    Serializer for post ShipmentBans model
    """
    class Meta:
        model = ShipmentBans
        fields = '__all__'
