import django_filters as filters

from apps.invoice.models import Invoice


class InvoiceFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    contract = filters.CharFilter(field_name='contract', lookup_expr='iexact')
    start_contract = filters.CharFilter(field_name='contract', lookup_expr='istartswith')
    end_contract = filters.CharFilter(field_name='contract', lookup_expr='iendswith')
    cont_contract = filters.CharFilter(field_name='contract', lookup_expr='icontains')
    number = filters.CharFilter(field_name='number', lookup_expr='iexact')
    start_number = filters.CharFilter(field_name='number', lookup_expr='istartswith')
    end_number = filters.CharFilter(field_name='number', lookup_expr='iendswith')
    cont_number = filters.CharFilter(field_name='number', lookup_expr='icontains')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    recipient = filters.CharFilter(field_name='recipient', lookup_expr='iexact')
    start_recipient = filters.CharFilter(field_name='recipient', lookup_expr='istartswith')
    end_recipient = filters.CharFilter(field_name='recipient', lookup_expr='iendswith')
    cont_recipient = filters.CharFilter(field_name='recipient', lookup_expr='icontains')
    shipper = filters.CharFilter(field_name='shipper', lookup_expr='iexact')
    start_shipper = filters.CharFilter(field_name='shipper', lookup_expr='istartswith')
    end_shipper = filters.CharFilter(field_name='shipper', lookup_expr='iendswith')
    cont_shipper = filters.CharFilter(field_name='shipper', lookup_expr='icontains')
    country = filters.CharFilter(field_name='country', lookup_expr='iexact')
    start_country = filters.CharFilter(field_name='country', lookup_expr='istartswith')
    end_country = filters.CharFilter(field_name='country', lookup_expr='iendswith')
    cont_country = filters.CharFilter(field_name='country', lookup_expr='icontains')
    currency = filters.CharFilter(field_name='currency', lookup_expr='iexact')
    start_currency = filters.CharFilter(field_name='currency', lookup_expr='istartswith')
    end_currency = filters.CharFilter(field_name='currency', lookup_expr='iendswith')
    cont_currency = filters.CharFilter(field_name='currency', lookup_expr='icontains')
    terms = filters.CharFilter(field_name='terms', lookup_expr='iexact')
    start_terms = filters.CharFilter(field_name='terms', lookup_expr='istartswith')
    end_terms = filters.CharFilter(field_name='terms', lookup_expr='iendswith')
    cont_terms = filters.CharFilter(field_name='terms', lookup_expr='icontains')
    container = filters.CharFilter(method='filter_container')
    start_container = filters.CharFilter(method='filter_start_container')
    end_container = filters.CharFilter(method='filter_end_container')
    cont_container = filters.CharFilter(method='filter_cont_container')

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
        label={
            "id": "ID",
            "contract": "Contract",
            "number": "Number",
            "date": "Date",
            "recipient": "Recipient",
            "shipper": "Shipper",
            "country": "Country",
            "currency": "Currency",
            "terms": "Terms",
            "container": "Container",
        }
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
