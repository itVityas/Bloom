import django_filters as filter

from .models import Products


class ProductFilter(filter.FilterSet):
    start_barcode = filter.CharFilter(field_name='barcode', lookup_expr='istartswith')

    class Meta:
        model = Products
        fields = [
            'id',
            'barcode',
            'start_barcode',
            'state',
            'nameplate',
            'quantity',
            'cleared'
        ]
