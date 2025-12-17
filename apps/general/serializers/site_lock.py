from rest_framework import serializers

from apps.general.models import SiteLock


class SiteLockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteLock
        fields = "__all__"
