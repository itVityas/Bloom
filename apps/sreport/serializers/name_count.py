from rest_framework import serializers

from apps.arrival.serializers.order import OrderSerializer
from apps.arrival.models import Order
from apps.shtrih.models import Products, Consignments, ProductTransitions
from apps.declaration.models import DeclaredItem
from django.db.models import Sum


class ModelNameCountSerializer(serializers.Serializer):
    model_name_id = serializers.IntegerField(write_only=True)
    order = serializers.SerializerMethodField()
    uncleared = serializers.SerializerMethodField()
    available_count = serializers.SerializerMethodField()

    def get_order(self, obj) -> dict:
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).values('declaration_number').distinct()
        orders = Order.objects.filter(
            containers__declarations__declaration_number__in=consigments).distinct()
        return OrderSerializer(orders, many=True).data

    def get_uncleared(self, obj) -> int:
        process_transitions_list = ProductTransitions.objects.all().values_list('old_product')
        process_transitions_list2 = ProductTransitions.objects.all().values_list('new_product')
        process_transitions_list = process_transitions_list.union(process_transitions_list2)
        products = Products.objects.filter(model__name__id=obj['model_name_id'], cleared__isnull=True)
        products = products.exclude(pk__in=process_transitions_list)
        return products.count()

    def get_available_count(self, obj) -> int:
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).values('declaration_number', 'G32').distinct()
        quantity = 0
        for item in consigments:
            declared_items = DeclaredItem.objects.filter(
                declaration__declaration_number=item['declaration_number'],
                ordinal_number=item['G32'])
            if declared_items:
                quantity += declared_items.aggregate(Sum('available_quantity'))['available_quantity__sum']
        return int(quantity)
