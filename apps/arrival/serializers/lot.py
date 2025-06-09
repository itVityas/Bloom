from rest_framework import serializers

from apps.arrival.models import Lot
from apps.invoice.models import TrainDoc
from apps.invoice.serializers.traindoc import TrainDocGetSerializer


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
