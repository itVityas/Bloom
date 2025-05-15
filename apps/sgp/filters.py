import django_filters as filters

from apps.sgp.models import ShipmentBans


class ShipmentBansFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    barcode = filters.CharFilter(field_name='barcode', lookup_expr='iexact')
    start_barcode = filters.CharFilter(field_name='barcode', lookup_expr='istartswith')
    end_barcode = filters.CharFilter(field_name='barcode', lookup_expr='iendswith')
    cont_barcode = filters.CharFilter(field_name='barcode', lookup_expr='icontains')

    class Meta:
        model = ShipmentBans
        fields = [
            'id',
            'is_active',
            'barcode',
            'start_barcode',
            'end_barcode',
            'cont_barcode',
        ]
