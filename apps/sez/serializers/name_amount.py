from rest_framework import serializers

from apps.omega.models import OBJ_ATTR_VALUES_1000004


class NameAmountSerializer(serializers.Serializer):
    name__id = serializers.IntegerField()
    name__short_name = serializers.SerializerMethodField()
    name__name = serializers.CharField()
    code = serializers.IntegerField()
    real_amount = serializers.IntegerField()
    weight_netto = serializers.SerializerMethodField()
    weight_brutto = serializers.SerializerMethodField()

    def get_name__short_name(self, obj) -> str:
        if obj.get('name__short_name', None) is None:
            return obj.get('name__name', None)
        return obj.get('name__short_name', None)

    def get_weight_netto(self, obj) -> float:
        weight = 0
        try:
            short_name = obj.get('name__short_name', None)
            omega_obj = OBJ_ATTR_VALUES_1000004.objects.using('oracle_db').filter(
                A_3607=short_name).first()
            if omega_obj:
                weight = omega_obj.A_2951
        finally:
            return weight

    def get_weight_brutto(self, obj) -> float:
        weight = 0
        try:
            short_name = obj.get('name__short_name', None)
            omega_obj = OBJ_ATTR_VALUES_1000004.objects.using('oracle_db').filter(
                A_3607=short_name).first()
            if omega_obj:
                weight = omega_obj.A_2950
        finally:
            return weight
