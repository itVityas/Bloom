import django_filters as filters

from .models import ClearanceInvoice


class ClearanceInvoiceFilter(filters.FilterSet):
    """
    Filter for ClearanceInvoice
    """
    id = filters.NumberFilter(
        field_name='id',
        lookup_expr='exact'
    )
    ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='icontains')
    series = filters.CharFilter(
        field_name='series',
        lookup_expr='icontains')
    recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='icontains')
    quantity_shipped = filters.NumberFilter(
        field_name='quantity_shipped',
        lookup_expr='exact')
    date_calc = filters.DateFilter(
        field_name='date_calc',
        lookup_expr='exact')

    class Meta:
        model = ClearanceInvoice
        fields = [
            'id',
            'ttn',
            'series',
            'recipient',
            'quantity_shipped',
            'date_calc',
            'date_cleared',
            'date_payments',
        ]
