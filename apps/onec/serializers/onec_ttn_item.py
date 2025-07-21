from rest_framework import serializers

from apps.onec.models import OneCTTNItem


class OneCTTNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTNItem
        fields = "__all__"
