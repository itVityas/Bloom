from rest_framework import serializers

from apps.sgp.models import ShipmentBans
from apps.shtrih.models import Models, Modules, Production_codes, Colors


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

    def get_production_code(self, obj) -> str:
        production_code_id = obj.production_code_id
        if production_code_id:
            try:
                return Production_codes.objects.filter(code=production_code_id).first().name
            except Exception as ex:
                print(ex)
                return ''
        return ''

    def get_model(self, obj) -> str:
        model_id = obj.model_id
        if model_id:
            try:
                return Models.objects.filter(id=model_id).first().name.short_name
            except Exception:
                return ''
        return ''

    def get_color(self, obj) -> str:
        color_id = obj.color_id
        if color_id:
            try:
                return Colors.objects.filter(id=color_id).first().russian_title
            except Exception:
                return ''
        return ''

    def get_module(self, obj) -> str:
        modules_id = obj.module_id
        if modules_id:
            try:
                return Modules.objects.filter(id=modules_id).first().number
            except Exception:
                return ''
        return ''


class ShipmentBansPostSerializer(serializers.ModelSerializer):
    """
    Serializer for post ShipmentBans model
    """
    class Meta:
        model = ShipmentBans
        fields = '__all__'
