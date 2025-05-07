from rest_framework import serializers

from apps.sgp.models import ShipmentBans
from apps.shtrih.models import ModelNames, Modules, Production_codes, Colors
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.serializers.production_code import ProductionCodeSerializer
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class ShipmentBansGetSerializer(serializers.ModelSerializer):
    """
    Serializer for get ShipmentBans model
    """
    production_code = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()

    class Meta:
        model = ShipmentBans
        fields = [
            'id',
            'order_number',
            'order_date',
            'message',
            'start_date',
            'end_date',
            'production_code',
            'model',
            'barcode',
            'color',
            'module',
            'shift',
            'assembly_date_from',
            'assembly_date_to',
            'pakaging_date_from',
            'pakaging_date_to',
            'is_active',
            'apply_to_belarus',
        ]

    def get_production_code(self, obj) -> dict:
        production_code_id = obj.production_code_id
        if production_code_id:
            try:
                productioin_code = Production_codes.objects.filter(code=production_code_id).first()
                return ProductionCodeSerializer(productioin_code).data
            except Exception as ex:
                print(ex)
                return {}
        return {}

    def get_model(self, obj) -> dict:
        model_id = obj.model_name_id
        if model_id:
            try:
                model_name = ModelNames.objects.filter(id=model_id).first()
                return ModelNamesSerializer(model_name).data
            except Exception:
                return {}
        return {}

    def get_color(self, obj) -> dict:
        color_id = obj.color_id
        if color_id:
            try:
                color = Colors.objects.filter(id=color_id).first()
                return ColorsSerializer(color).data
            except Exception:
                return {}
        return {}

    def get_module(self, obj) -> dict:
        modules_id = obj.module_id
        if modules_id:
            try:
                module = Modules.objects.filter(id=modules_id).first().number
                return ModulesSerializer(module).data
            except Exception:
                return {}
        return {}


class ShipmentBansPostSerializer(serializers.ModelSerializer):
    """
    Serializer for post ShipmentBans model
    """
    class Meta:
        model = ShipmentBans
        fields = '__all__'
