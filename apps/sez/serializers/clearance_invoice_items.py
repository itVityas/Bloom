from rest_framework import serializers
from django.db.models import Sum, IntegerField, OuterRef, F, Subquery
from django.db.models.functions import Coalesce

from apps.sez.models import ClearanceInvoiceItems, ClearedItem
from apps.shtrih.serializers.model_name import ModelNamesSerializer
from apps.shtrih.models import Models, Products
from apps.declaration.models import DeclaredItem


class ClearanceInvoiceItemsSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoiceItems model.
    """
    class Meta:
        model = ClearanceInvoiceItems
        fields = '__all__'


class ClearanceInvoiceItemsFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClearanceInvoiceItems model + full fields
    """
    model_name_object = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    model_code = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()
    real_amount = serializers.SerializerMethodField()

    class Meta:
        model = ClearanceInvoiceItems
        fields = [
            'id',
            'quantity',
            'clearance_invoice',
            'declared_item',
            'model_name_object',
            'model_name',
            'model_code',
            'unit_name',
            'real_amount',
        ]

    def get_model_name_object(self, obj):
        return ModelNamesSerializer(obj.model_name_id).data

    def get_model_name(self, obj) -> str:
        model_name = obj.model_name_id
        if obj.declared_item:
            return obj.declared_item.name
        if model_name:
            return model_name.short_name
        return ''

    def get_model_code(self, obj) -> str:
        model_name_id = obj.model_name_id
        if obj.declared_item:
            return None
        if model_name_id:
            model = Models.objects.filter(name=model_name_id).first()
            if model:
                return model.code
        return None

    def get_unit_name(self, obj) -> str:
        if obj.declared_item:
            return obj.declared_item.unit_code
        return None

    def get_real_amount(self, obj) -> float:
        declaration_item = obj.declared_item
        if not declaration_item:
            count = Products.objects.filter(
                cleared__isnull=True,
                model__name__id=obj.model_name_id.id
            ).values('barcode').distinct().count()
            return count

        cleared_items_subquery = ClearedItem.objects.filter(
            declared_item_id=OuterRef('id')
        ).values('declared_item_id').annotate(
            total_cleared=Sum('quantity', output_field=IntegerField())
        ).values('total_cleared').order_by()

        real_amount = DeclaredItem.objects.filter(id=declaration_item.id).annotate(
            real_amount=F('quantity') - Coalesce(Subquery(cleared_items_subquery), 0)
        ).filter(
            real_amount__gt=0
        ).values(
            'real_amount',
        ).first()
        return real_amount['real_amount'] if real_amount else 0
