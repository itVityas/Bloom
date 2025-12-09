from rest_framework import serializers

from apps.sez.models import ClearanceInvoiceItems
from apps.shtrih.serializers.model_name import ModelNamesSerializer
from apps.shtrih.models import Models, Products, ProductTransitions
from apps.declaration.models import Declaration


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
    real_amount = serializers.SerializerMethodField()

    class Meta:
        model = ClearanceInvoiceItems
        fields = [
            'id',
            'quantity',
            'clearance_invoice',
            'model_name_object',
            'model_name',
            'model_code',
            'real_amount',
        ]

    def get_model_name_object(self, obj):
        return ModelNamesSerializer(obj.model_name_id).data

    def get_model_name(self, obj) -> str:
        model_name = obj.model_name_id
        if model_name:
            return model_name.short_name
        return ''

    def get_model_code(self, obj) -> str:
        model_name_id = obj.model_name_id
        if model_name_id:
            model = Models.objects.filter(name=model_name_id).first()
            if model:
                return model.code
        return None

    def get_real_amount(self, obj) -> float:
        order_list = obj.clearance_invoice.order.values_list('id', flat=True)
        is_gifted = obj.clearance_invoice.is_gifted
        process_transitions_list = ProductTransitions.objects.all().values_list('old_product')
        products = Products.objects.filter(model__name__id=obj.model_name_id.id, cleared__isnull=True)

        model = Models.objects.filter(name=obj.model_name_id.id).first()
        if model.production_code.code != 400:
            return products.count()
        if order_list:
            # get list of decl in order: [('07260/52003398',), ('07260/52001406',),
            # ('07260/52001405',), ('07260/52001449',), ('07260/52001402',)]
            declaration_numbers = Declaration.objects.filter(
                container__order__id__in=order_list, is_use=True).values_list('declaration_number')
            products = products.filter(consignment__declaration_number__in=declaration_numbers)
        if is_gifted:
            declaration_numbers = Declaration.objects.filter(gifted=True, is_use=True).values_list('declaration_number')
            products = products.filter(consignment__declaration_number__in=declaration_numbers)
        else:
            declaration_numbers = Declaration.objects.filter(
                gifted=False).values_list('declaration_number')
            products = products.filter(consignment__declaration_number__in=declaration_numbers)
        products = products.exclude(pk__in=process_transitions_list)
        return products.count()
