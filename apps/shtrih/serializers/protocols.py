from rest_framework import serializers

from apps.shtrih.models import Protocols


class ProtocolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocols
        fields = "__all__"
