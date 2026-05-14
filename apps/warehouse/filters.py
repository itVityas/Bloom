import django_filters as filters

from apps.warehouse.models import (
    WarehouseTTN,
    WarehouseDo,
    BarcodlessProducts,
    BarcodlessDo,
)


class WarehouseTTNFilter(filters.FilterSet):
    ttn_number = filters.CharFilter(field_name='ttn_number', lookup_expr='iexact')
    ttn_number_start = filters.CharFilter(field_name='ttn_number', lookup_expr='istartswith')
    ttn_number_end = filters.CharFilter(field_name='ttn_number', lookup_expr='iendswith')
    ttn_number_cont = filters.CharFilter(field_name='ttn_number', lookup_expr='icontains')
    is_close = filters.BooleanFilter(field_name='is_close')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    onec_number = filters.CharFilter(field_name='onec_ttn__number', lookup_expr='iexact')
    onec_series = filters.CharFilter(field_name='onec_ttn__series', lookup_expr='iexact')
    warehouse_action_id = filters.NumberFilter(field_name='warehouse_action_id', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('ttn_number', 'ttn_number'),
            ('is_close', 'is_close'),
            ('date', 'date'),
            ('warehouse', 'warehouse_id'),
            ('warehouse_action', 'warehouse_action_id'),
            ('user', 'user_id'),
            ('id', 'id'),
            ('create_at', 'create_at'),
            ('update_at', 'update_at'),
            ('barcode', 'warehouse_do__product__barcode'),
            ('warehouse_action_id', 'warehouse_action_id'),
        ),
    )

    class Meta:
        model = WarehouseTTN
        fields = (
            'ttn_number',
            'ttn_number_start',
            'ttn_number_end',
            'ttn_number_cont',
            'is_close',
            'date',
            'onec_number',
            'onec_series',
            'warehouse_action_id',
        )


class WarehouseDoFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')
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
            'warehouse_ttn',
        )


class BarcodlessProductsFilter(filters.FilterSet):
    pk = filters.NumberFilter(field_name='pk', lookup_expr='exact')
    model_name_id = filters.NumberFilter(field_name='model_name_id', lookup_expr='exact')
    model_name = filters.CharFilter(field_name='model_name__name', lookup_expr='iexact')
    model_name_start = filters.CharFilter(field_name='model_name__name', lookup_expr='istartswith')
    model_name_end = filters.CharFilter(field_name='model_name__name', lookup_expr='iendswith')
    warehouse_id = filters.NumberFilter(field_name='warehouse_id', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('pk', 'pk'),
            ('model_name_id', 'model_name_id'),
            ('warehouse_id', 'warehouse_id'),
            ('create_at', 'create_at'),
            ('update_at', 'update_at'),
        ),
    )

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
    barcode_product_id = filters.NumberFilter(field_name='barcode_product_id', lookup_expr='exact')
    warehouse_ttn_id = filters.NumberFilter(field_name='warehouse_ttn_id', lookup_expr='exact')
    ttn_number = filters.CharFilter(field_name='warehouse_ttn__ttn_number', lookup_expr='iexact')

    ordering = filters.OrderingFilter(
        fields=(
            ('pk', 'pk'),
            ('barcode_product_id', 'barcode_product_id'),
            ('create_at', 'create_at'),
            ('update_at', 'update_at'),
        ),
    )

    class Meta:
        model = BarcodlessDo
        fields = (
            'pk',
            'barcode_product_id',
            'warehouse_ttn_id',
            'ttn_number',
        )
