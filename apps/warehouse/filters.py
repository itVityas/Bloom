import django_filters as filters

from apps.warehouse.models import (
    WarehouseTTN,
    WarehouseDo,
    BarcodlessProducts,
    BarcodlessDo,
)


class WarehouseTTNFilter(filters.FilterSet):
    number = filters.CharFilter(field_name='number', lookup_expr='iexact')
    number_start = filters.CharFilter(field_name='number', lookup_expr='istartswith')
    number_end = filters.CharFilter(field_name='number', lookup_expr='iendswith')
    number_cont = filters.CharFilter(field_name='number', lookup_expr='icontains')
    is_close = filters.BooleanFilter(field_name='is_close')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    onec_number = filters.CharFilter(field_name='onec_ttn__number', lookup_expr='iexact')
    onec_series = filters.CharFilter(field_name='onec_ttn__series', lookup_expr='iexact')

    ordering = filters.OrderingFilter(
        fields=(
            ('number', 'number'),
            ('is_close', 'is_close'),
            ('date', 'date'),
            ('warehouse', 'warehouse_id'),
            ('warehouse_action', 'warehouse_action_id'),
            ('user', 'user_id'),
            ('id', 'id'),
            ('create_at', 'create_at'),
            ('update_at', 'update_at'),
        ),
    )

    class Meta:
        model = WarehouseTTN
        fields = (
            'number',
            'number_start',
            'number_end',
            'number_cont',
            'is_close',
            'date',
            'onec_number',
            'onec_series',
        )


class WarehouseDoFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')
    warehouse_product = filters.NumberFilter(
        field_name='warehouse_product', lookup_expr='exact')
    warehouse_ttn = filters.NumberFilter(
        field_name='warehouse_ttn', lookup_expr='exact')
    user = filters.NumberFilter(field_name='user', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('user', 'user_id'),
            ('warehouse_product', 'warehouse_product_id'),
            ('warehouse_ttn', 'warehouse_ttn_id')
        ),
    )

    class Meta:
        model = WarehouseDo
        fields = (
            'id',
            'quantity',
            'create_at',
            'update_at',
            'user',
            'warehouse_product',
            'warehouse_ttn',
        )


class BarcodlessProductsFilter(filters.FilterSet):
    pk = filters.NumberFilter(field_name='pk', lookup_expr='exact')
    model_name_id = filters.NumberFilter(field_name='model_name_id', lookup_expr='exact')
    model_name = filters.CharFilter(field_name='model_name__name', lookup_expr='iexact')
    model_name_start = filters.CharFilter(field_name='model_name__name', lookup_expr='istartswith')
    model_name_end = filters.CharFilter(field_name='model_name__name', lookup_expr='iendswith')
    warehouse_id = filters.NumberFilter(field_name='warehouse_id', lookup_expr='exact')

    class Meta:
        model = BarcodlessProducts
        fields = (
            'pk',
            'model_name_id',
            'model_name',
            'model_name_start',
            'model_name_end',
            'warehouse_id',
        )


class BarcodlessDoFilter(filters.FilterSet):
    pk = filters.NumberFilter(field_name='pk', lookup_expr='exact')
    product_id = filters.NumberFilter(field_name='product_id', lookup_expr='exact')
    warehouse_ttn_id = filters.NumberFilter(field_name='warehouse_ttn_id', lookup_expr='exact')
    ttn_number = filters.CharFilter(field_name='warehouse_ttn__ttn_number', lookup_expr='iexact')

    class Meta:
        model = BarcodlessDo
        fields = (
            'pk',
            'product_id',
            'warehouse_ttn_id',
            'ttn_number',
        )
