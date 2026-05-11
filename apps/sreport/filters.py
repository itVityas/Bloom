import django_filters as filters
from django.db.models import Sum

from apps.sreport.models import ReportStorage, WarehouseTTNBarcode
from apps.shtrih.models import ModelNames


class ReportStorageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    start_name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    end_name = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    cont_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    production_code = filters.NumberFilter(method='filter_production_code')
    warehouse_id = filters.NumberFilter(method='filter_warehouse_id')

    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('uncleared', 'uncleared'),
            ('cleared', 'cleared'),
            ('simple', 'simple'),
            ('compensation', 'compensation'),
        ),
    )

    class Meta:
        model = ReportStorage
        fields = [
            'name',
            'start_name',
            'end_name',
            'cont_name',
            'production_code',
            'warehouse_id',
        ]

    def filter_production_code(self, queryset, name, value):
        model_names = ModelNames.objects.distinct().filter(
            models__production_code__code=value).values_list('id', flat=True)
        return queryset.filter(model_name_id__in=model_names)

    def filter_warehouse_id(self, queryset, name, value):
        if value == 0:
            return queryset.values(
                'model_name_id', 'name'
            ).annotate(
                uncleared=Sum('uncleared'),
                cleared=Sum('cleared'),
                simple=Sum('simple'),
                compensation=Sum('compensation')
            )
        return queryset.filter(warehouse_id=value)


class WarehouseTTNBarcodeFilter(filters.FilterSet):
    model_name_name = filters.NumberFilter(field_name='model_name_id')
    warehouse_name = filters.NumberFilter(field_name='warehouse_id')
    user_fio = filters.CharFilter(field_name='user_fio')
    warehouse_do_create_at = filters.DateTimeFilter(field_name='warehouse_do_create_at')
    warehouse_ttn_ttn_number = filters.CharFilter(field_name='warehouse_ttn_ttn_number')

    ordering = filters.OrderingFilter(
        fields=(
            ('product_barcode', 'product_barcode'),
            ('model_name_name', 'model_name_name'),
            ('warehouse_name', 'warehouse_name'),
            ('warehouse_do_create_at', 'warehouse_do_create_at'),
            ('warehouse_ttn_ttn_number', 'warehouse_ttn_ttn_number'),
            ('user_fio', 'user_fio'),
        ),
    )

    class Meta:
        model = WarehouseTTNBarcode
        fields = [
            'model_name_id',
            'warehouse_id',
            'warehouse_ttn_ttn_number',
            'user_fio',
            'warehouse_do_create_at',
        ]
