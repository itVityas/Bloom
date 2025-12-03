from rest_framework import serializers

from apps.arrival.serializers.order import OrderSerializer
from apps.arrival.models import Order
from apps.shtrih.models import Products, Consignments, ProductTransitions
from apps.declaration.models import Declaration
from django.db.models import Sum


class ModelNameOrderSerializer(serializers.Serializer):
    model_name_id = serializers.IntegerField(write_only=True)
    order_id = serializers.IntegerField(write_only=True)
    order = uncleared = serializers.SerializerMethodField()
    uncleared = serializers.SerializerMethodField()
    available_count = serializers.SerializerMethodField()

    def get_order(self, obj) -> dict:
        return OrderSerializer(Order.objects.get(pk=obj['order_id'])).data

    def get_available_count(self, obj) -> int:
        order_decl = Declaration.objects.filter(
            container__order__id=obj['order_id']).values('declaration_number').distinct()
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id'],
            declaration_number__in=order_decl).values('declaration_number', 'G32').exclude(is_gift=1).distinct()
        if not consigments:
            return 0
        quantity = consigments.aggregate(Sum('quantity'))['quantity__sum'] \
            - consigments.aggregate(Sum('used_quantity'))['used_quantity__sum']
        return int(quantity)

    def get_uncleared(self, obj) -> int:
        order_decl = Declaration.objects.filter(
            container__order__id=obj['order_id']).values('declaration_number').distinct()
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id'],
            declaration_number__in=order_decl).exclude(is_gift=1).distinct()
        process_transitions_list = ProductTransitions.objects.all().values_list('old_product')
        process_transitions_list2 = ProductTransitions.objects.all().values_list('new_product')
        process_transitions_list = process_transitions_list.union(process_transitions_list2)
        products = Products.objects.filter(model__name__id=obj['model_name_id'], cleared__isnull=True)
        products = products.exclude(pk__in=process_transitions_list, consignment__in=consigments)
        return products.count()


class ModelNameCountSerializer(serializers.Serializer):
    model_name_id = serializers.IntegerField(write_only=True)
    order = serializers.SerializerMethodField()
    without_order_uncleared = serializers.SerializerMethodField()
    without_order_available = serializers.SerializerMethodField()

    def get_order(self, obj) -> dict:
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).values('declaration_number').exclude(is_gift=1).distinct()
        orders_id = Order.objects.filter(
            containers__declarations__declaration_number__in=consigments).values_list('id', flat=True).distinct()
        data = []
        for ids in orders_id:
            data.append({'model_name_id': obj['model_name_id'], 'order_id': ids})
        return ModelNameOrderSerializer(
            data, many=True).data

    def get_without_order_uncleared(self, obj) -> int:
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).values('declaration_number').exclude(is_gift=1).distinct()
        orders_id = Order.objects.filter(
            containers__declarations__declaration_number__in=consigments).values_list('id', flat=True).distinct()
        decl_numbers = Declaration.objects.filter(
            container__order__in=orders_id).values_list('declaration_number', flat=True).distinct()
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id'], declaration_number__in=decl_numbers).exclude(is_gift=1).distinct()
        products = Products.objects.filter(
            model__name__id=obj['model_name_id'], cleared__isnull=True)
        products = products.exclude(consignment__in=consigments)
        return products.count()

    def get_without_order_available(self, obj) -> int:
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).values('declaration_number').exclude(is_gift=1).distinct()
        orders_id = Order.objects.filter(
            containers__declarations__declaration_number__in=consigments).values_list('id', flat=True).distinct()
        decl_numbers = Declaration.objects.filter(
            container__order__in=orders_id).values_list('declaration_number', flat=True).distinct()
        consigments = Consignments.objects.filter(
            model_name__id=obj['model_name_id']).exclude(
                declaration_number__in=decl_numbers).exclude(is_gift=1).distinct()
        if not consigments:
            return 0
        quantity = consigments.aggregate(Sum('quantity'))['quantity__sum'] \
            - consigments.aggregate(Sum('used_quantity'))['used_quantity__sum']
        return int(quantity)
