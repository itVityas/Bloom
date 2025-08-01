from rest_framework import serializers

from apps.warehouse.models import (
    Pallet,
)
from apps.warehouse.utils.generate_barcode import generate_barcode


class PalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = "__all__"


class PalletGenerateSerializer(serializers.ModelSerializer):
    """barcode: 5: model + 2: month + 2: year + 3: col + 8: ttn_number
    """
    ttn_number = serializers.CharField(write_only=True, required=True)
    barcode = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Pallet
        fields = "__all__"

    def create(self, validated_data):
        ttn_number = validated_data.pop('ttn_number', None)
        if not ttn_number:
            raise serializers.ValidationError('Не указан номер ТТН')

        barcode = generate_barcode(ttn_number=ttn_number)
        if barcode.find('Error') != -1 or not isinstance(barcode, str):
            raise serializers.ValidationError('Не удалось сгенерировать штрих-код' + barcode)

        pallet = Pallet.objects.filter(barcode=barcode).first()
        if pallet:
            return pallet

        return Pallet.objects.create(
            barcode=barcode
        )
