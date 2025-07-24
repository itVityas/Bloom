from rest_framework import serializers

from apps.warehouse.models import (
    Pallet,
    WarehouseTTN,
    WarehouseDo
)
from apps.shtrih.models import Models
from apps.warehouse.utils.len_word import LenWord


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
        warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
        if not warehouse_ttn:
            raise serializers.ValidationError('ТТН не найден')

        warehouse_do = WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn)
        if not warehouse_do:
            raise serializers.ValidationError('ТТН не найден')

        col = warehouse_do.count()
        col = LenWord(str(col), 3)  # we need col with 3 character

        ttn_date = warehouse_ttn.date
        month = ttn_date.month
        month = LenWord(str(month), 2)  # we need month with 2 character
        year = ttn_date.year
        year = LenWord(str(year), 2)  # we need year with 2 character

        model = Models.objects.filter(id=warehouse_do.first().warehouse_product.product.model.pk).first()
        model = LenWord(str(model.code), 5)  # we need model with 5 character

        ttn_number = LenWord(str(ttn_number), 8)  # we need ttn_number with 8 character

        barcode = model + month + year + col + ttn_number
        if len(barcode) < 18:
            raise serializers.ValidationError('Неверный штрихкод')

        return Pallet.objects.create(
            barcode=barcode
        )
