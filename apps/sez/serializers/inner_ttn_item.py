from rest_framework import serializers

from apps.sez.models import InnerTTNItems


class InnerTTNItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerTTNItems
        fields = "__all__"
