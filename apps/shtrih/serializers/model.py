from rest_framework import serializers

from apps.shtrih.models import Models


class ModelsSerializer(serializers.ModelSerializer):
    omega_model_id = serializers.IntegerField()
    omega_variant_id = serializers.IntegerField()
    production_code = serializers.SerializerMethodField()
    code = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    diagonal = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_warranty = serializers.IntegerField()
    storage_warranty = serializers.IntegerField()
    variant_code = serializers.CharField(max_length=20)
    design_code = serializers.CharField(max_length=20)
    letter_part = serializers.CharField(max_length=25)
    numeric_part = serializers.CharField(max_length=20)
    execution_part = serializers.CharField(max_length=10)
    create_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()

    class Meta:
        model = Models
        fields = [
            'id',
            'omega_model_id',
            'omega_variant_id',
            'production_code',
            'code',
            'name',
            'diagonal',
            'weight',
            'quantity',
            'product_warranty',
            'storage_warranty',
            'variant_code',
            'design_code',
            'letter_part',
            'numeric_part',
            'execution_part',
            'create_at',
            'update_at',
        ]

    def get_production_code(self, obj) -> str:
        try:
            return obj.production_code.name
        except Exception:
            return ''

    def get_name(self, obj) -> str:
        short_name = obj.name.short_name
        if short_name:
            return short_name
        else:
            return obj.name.name
