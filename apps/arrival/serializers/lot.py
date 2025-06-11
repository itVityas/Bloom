from rest_framework import serializers

from apps.arrival.models import Lot, LotModel
from apps.invoice.models import TrainDoc
from apps.invoice.serializers.traindoc import TrainDocGetSerializer
from apps.arrival.serializers.lot_model import LotModelPostSerializer


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
    traindoc = serializers.SerializerMethodField()
    lot_model = serializers.SerializerMethodField()

    class Meta:
        model = Lot
        fields = '__all__'

    def get_traindoc(self, obj) -> dict:
        """
        Get the train document associated with the lot.
        """
        traindoc = TrainDoc.objects.filter(lot=obj).first()
        if traindoc:
            return TrainDocGetSerializer(traindoc).data
        return None

    def get_lot_model(self, obj) -> dict:
        """
        Get the lot model associated with the lot.
        """
        lot_model = LotModel.objects.filter(lot=obj)
        if lot_model:
            return LotModelPostSerializer(lot_model, many=True).data
        return None
