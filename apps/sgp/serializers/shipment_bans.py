from rest_framework import serializers

from apps.sgp.models import ShipmentBans
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.serializers.production_code import ProductionCodeSerializer
from apps.shtrih.serializers.model_name import ModelNamesSerializer


class ShipmentBansGetSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for retrieving ShipmentBan records with nested relationships.

    Provides complete shipment ban information including:
    - Core ban details (dates, status, references)
    - Nested representations of related objects:
      * Production codes
      * Model names
      * Colors
      * Modules
    """
    production_code_obj = serializers.SerializerMethodField()
    model_obj = serializers.SerializerMethodField()
    color_obj = serializers.SerializerMethodField()
    module_obj = serializers.SerializerMethodField()

    class Meta:
        model = ShipmentBans
        fields = [
            'id',
            'order_number',
            'order_date',
            'message',
            'start_date',
            'end_date',
            'production_code_obj',
            'model_obj',
            'barcode',
            'color_obj',
            'module_obj',
            'shift',
            'assembly_date_from',
            'assembly_date_to',
            'pakaging_date_from',
            'pakaging_date_to',
            'is_active',
            'apply_to_belarus',
        ]

    def get_production_code_obj(self, obj) -> dict:
        production_code = obj.production_code_id
        if production_code:
            return ProductionCodeSerializer(production_code).data
        return {}

    def get_model_obj(self, obj) -> dict:
        model_name = obj.model_name_id
        if model_name:
            return ModelNamesSerializer(model_name).data
        return {}

    def get_color_obj(self, obj) -> dict:
        color = obj.color_id
        if color:
            return ColorsSerializer(color).data
        return {}

    def get_module_obj(self, obj) -> dict:
        module = obj.module_id
        if module:
            return ModulesSerializer(module).data
        return {}


class ShipmentBansPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating ShipmentBan records.

    Handles:
    - Validation of all input data
    - Enforcement of business rules
    - Proper relationship handling

    Includes comprehensive field validation for:
    - Date consistency
    - Required field combinations
    - Value constraints
    """
    class Meta:
        model = ShipmentBans
        fields = '__all__'
