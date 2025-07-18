import django_filters as filters

from apps.warehouse.models import (
    WarehouseProduct,
    Palleting,
    WarehouseTTN,
    WarehouseProductHistory
)


class WarehouseProductFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name='is_active')
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='exact')
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='exact')
    update_at = filters.DateFilter(field_name='update_at', lookup_expr='icontains')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('product', 'product_id'),
            ('warehouse', 'warehouse_id'),
            ('warehouse_action', 'warehouse_acton_id'),
            ('warehouse_ttn', 'warehouse_ttn'),
            ('update_at', 'update_at'),
            ('create_at', 'create_at'),
            ('quantity', 'quantity'),
            ('user', 'user_id'),
        ),
    )

    class Meta:
        model = WarehouseProduct
        fields = (
            'is_active',
            'quantity',
            'create_at',
            'update_at',
        )


class WarehouseProductHistoryFilter(WarehouseProductFilter):
    class Meta:
        model = WarehouseProductHistory
        fields = (
            'is_active',
            'quantity',
            'create_at',
            'update_at',
        )


class PalletingFilter(filters.FilterSet):
    create_at = filters.DateFilter(field_name='create_at', lookup_expr='icontains')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('pallet', 'pallet_id'),
            ('warehouse_product', 'warehouse_product_id'),
            ('create_at', 'create_at'),
            ('user', 'user_id'),
        ),
    )

    class Meta:
        model = Palleting
        fields = (
            'create_at',
        )


class WarehouseTTNFilter(filters.FilterSet):
    number = filters.CharFilter(field_name='number', lookup_expr='iexact')
    number_start = filters.CharFilter(field_name='number', lookup_expr='istartswith')
    number_end = filters.CharFilter(field_name='number', lookup_expr='iendswith')
    number_cont = filters.CharFilter(field_name='number', lookup_expr='icontains')
    is_close = filters.BooleanFilter(field_name='is_close')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('number', 'number'),
            ('is_close', 'is_close'),
            ('date', 'date'),
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
        )
