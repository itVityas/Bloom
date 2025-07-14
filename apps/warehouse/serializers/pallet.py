from rest_framework import serializers

from apps.warehouse.models import Pallet


class PalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"
