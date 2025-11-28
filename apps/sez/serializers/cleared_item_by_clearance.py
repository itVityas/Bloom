from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from apps.sez.models import ClearedItem


class ClearedItemListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing ClearedItem entries for a given invoice,
    including related declaration and declared item data.
    """
    declaration_number = serializers.CharField(
        source='declared_item_id.declaration.declaration_number',
        read_only=True
    )
    permit_number = serializers.CharField(
        source='declared_item_id.declaration.permit_number',
        read_only=True
    )
    declaration_date = serializers.DateField(
        source='declared_item_id.declaration.declaration_date',
        read_only=True
    )
    item_name = serializers.CharField(
        source='declared_item_id.name',
        read_only=True
    )
    ordinal_number = serializers.IntegerField(
        source='declared_item_id.ordinal_number',
        read_only=True
    )
    measurement = serializers.CharField(
        source='declared_item_id.measurement',
        read_only=True
    )
    sum_cost = serializers.SerializerMethodField()
    declared_available_quantity = serializers.IntegerField(
        source='declared_item_id.available_quantity',
        read_only=True
    )
    declared_item_quantity = serializers.IntegerField(
        source='declared_item_id.items_quantity',
        read_only=True
    )

    class Meta:
        model = ClearedItem
        fields = [
            'id',
            'declaration_number',
            'permit_number',
            'declaration_date',
            'item_name',
            'ordinal_number',
            'quantity',
            'measurement',
            'sum_cost',
            'declared_item_id',
            'declared_available_quantity',
            'declared_item_quantity',
        ]

    @extend_schema_field(serializers.FloatField())
    def get_sum_cost(self, obj) -> float:
        """
        Calculate total cost for this cleared line as quantity * declared_item.cost.
        """
        declared = obj.declared_item_id
        if declared and declared.cost is not None:
            return round(float(obj.quantity) * (float(declared.cost) / float(declared.items_quantity)), 2)
        return 0.0
