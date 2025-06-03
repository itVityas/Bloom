import django_filters as filters

from apps.invoice.models import Invoice


class InvoiceFilter(filters.FilterSet):
    """
    Advanced filtering for Invoice records with support for:
    - Exact matches and partial matches (prefix/suffix/contains)
    - Case-insensitive text matching
    - Date filtering
    - Related container filtering
    - Custom ordering

    Example Usage:
        /api/invoices/?contract__startswith=CNT&ordering=-date
        /api/invoices/?container=CONTAINER123&currency=USD
    """
    id = filters.NumberFilter(
        field_name='id',
        lookup_expr='exact',
        help_text=("Filter by exact ID match"))
    contract = filters.CharFilter(
        field_name='contract',
        lookup_expr='iexact',
        help_text=("Filter by exact contract number (case-insensitive)"))
    start_contract = filters.CharFilter(
        field_name='contract',
        lookup_expr='istartswith',
        help_text=("Filter by contract number starting with (case-insensitive)"))
    end_contract = filters.CharFilter(
        field_name='contract',
        lookup_expr='iendswith',
        help_text=("Filter by contract number ending with (case-insensitive)"))
    cont_contract = filters.CharFilter(
        field_name='contract',
        lookup_expr='icontains',
        help_text=("Filter by contract number containing (case-insensitive)"))
    number = filters.CharFilter(
        field_name='number',
        lookup_expr='iexact',
        help_text=("Filter by exact invoice number (case-insensitive)"))
    start_number = filters.CharFilter(
        field_name='number',
        lookup_expr='istartswith',
        help_text=("Filter by invoice number starting with (case-insensitive)"))
    end_number = filters.CharFilter(
        field_name='number',
        lookup_expr='iendswith',
        help_text=("Filter by invoice number ending with (case-insensitive)"))
    cont_number = filters.CharFilter(
        field_name='number',
        lookup_expr='icontains',
        help_text=("Filter by invoice number containing (case-insensitive)"))
    date = filters.DateFilter(
        field_name='date',
        lookup_expr='exact',
        help_text=("Filter by exact invoice date"))
    recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='iexact',
        help_text=("Filter by exact recipient name (case-insensitive)"))
    start_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='istartswith',
        help_text=("Filter by recipient name starting with (case-insensitive)"))
    end_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='iendswith',
        help_text=("Filter by recipient name ends with (case-insensitive)"))
    cont_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='icontains',
        help_text=("Filter by recipient name containing (case-insensitive)"))
    shipper = filters.CharFilter(field_name='shipper', lookup_expr='iexact')
    start_shipper = filters.CharFilter(field_name='shipper', lookup_expr='istartswith')
    end_shipper = filters.CharFilter(field_name='shipper', lookup_expr='iendswith')
    cont_shipper = filters.CharFilter(field_name='shipper', lookup_expr='icontains')
    country = filters.CharFilter(
        field_name='country',
        lookup_expr='iexact',
        help_text=("Filter by exact country name (case-insensitive)"))
    start_country = filters.CharFilter(
        field_name='country',
        lookup_expr='istartswith',
        help_text=("Filter by country name starting with (case-insensitive)"))
    end_country = filters.CharFilter(
        field_name='country',
        lookup_expr='iendswith',
        help_text=("Filter by country name ends with (case-insensitive)"))
    cont_country = filters.CharFilter(
        field_name='country',
        lookup_expr='icontains',
        help_text=("Filter by country name containing (case-insensitive)"))
    currency = filters.CharFilter(
        field_name='currency',
        lookup_expr='iexact',
        help_text=("Filter by exact currency code (case-insensitive)"))
    start_currency = filters.CharFilter(
        field_name='currency',
        lookup_expr='istartswith',
        help_text=("Filter by currency code starting with(case-insensitive)"))
    end_currency = filters.CharFilter(
        field_name='currency',
        lookup_expr='iendswith',
        help_text=("Filter by currency code ending with(case-insensitive)"))
    cont_currency = filters.CharFilter(
        field_name='currency',
        lookup_expr='icontains',
        help_text=("Filter by currency code containing(case-insensitive)"))
    terms = filters.CharFilter(
        field_name='terms',
        lookup_expr='iexact',
        help_text=("Filter by exact payment terms (case-insensitive)"))
    start_terms = filters.CharFilter(
        field_name='terms',
        lookup_expr='istartswith',
        help_text=("Filter by payment terms starting with (case-insensitive)"))
    end_terms = filters.CharFilter(
        field_name='terms',
        lookup_expr='iendswith',
        help_text=("Filter by payment terms ending with (case-insensitive)"))
    cont_terms = filters.CharFilter(
        field_name='terms',
        lookup_expr='icontains',
        help_text=("Filter by payment terms containing with (case-insensitive)"))
    container = filters.CharFilter(
        method='filter_container',
        help_text=("Filter by exact container name (case-insensitive)"))
    start_container = filters.CharFilter(
        method='filter_start_container',
        help_text=("Filter by container name starting with (case-insensitive)"))
    end_container = filters.CharFilter(
        method='filter_end_container',
        help_text=("Filter by container name ending with (case-insensitive)"))
    cont_container = filters.CharFilter(
        method='filter_cont_container',
        help_text=("Filter by container name containing (case-insensitive)"))

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('contract', 'contract'),
            ('number', 'number'),
            ('date', 'date'),
            ('recipient', 'recipient'),
            ('shipper', 'shipper'),
            ('country', 'country'),
            ('currency', 'currency'),
            ('terms', 'terms'),
            ('container', 'container'),
        ),
    )

    class Meta:
        model = Invoice
        fields = [
            'id',
            'contract',
            'start_contract',
            'end_contract',
            'cont_contract',
            'number',
            'start_number',
            'end_number',
            'cont_number',
            'date',
            'recipient',
            'start_recipient',
            'end_recipient',
            'cont_recipient',
            'shipper',
            'start_shipper',
            'end_shipper',
            'cont_shipper',
            'country',
            'start_country',
            'end_country',
            'cont_country',
            'currency',
            'start_currency',
            'end_currency',
            'cont_currency',
            'terms',
            'start_terms',
            'end_terms',
            'cont_terms',
        ]

    def filter_container(self, queryset, name, value):
        return queryset.filter(container__name__iexact=value).distinct()

    def filter_start_container(self, queryset, name, value):
        return queryset.filter(container__name__istartswith=value).distinct()

    def filter_end_container(self, queryset, name, value):
        return queryset.filter(container__name__iendswith=value).distinct()

    def filter_cont_container(self, queryset, name, value):
        return queryset.filter(container__name__icontains=value).distinct()
