from rest_framework import serializers

from apps.onec.models import OneCTTN
from apps.onec.serializers.onec_ttn_item import OneCTTNItemSerializer


class OneCTTNPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneCTTN
        fields = "__all__"


class OneCTTNGetSerializer(serializers.ModelSerializer):
    items = OneCTTNItemSerializer(many=True, read_only=True)

    class Meta:
        model = OneCTTN
        fields = "__all__"
