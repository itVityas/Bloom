import django_filters as filters

from .models import ClearanceInvoice, InnerTTN


class ClearanceInvoiceFilter(filters.FilterSet):
    """
    Advanced filtering for ClearanceInvoice records.

    Supports:
    - Exact matches and partial matches (prefix/suffix/contains)
    - Case-insensitive text matching
    - Date filtering
    - Null checks for optional fields

    Example Usage:
        /api/clearance-invoices/?series__startswith=INV&date_calc__isnull=false
    """
    id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iexact',
        help_text=("Filter by exact ID match")
    )
    cont_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='icontains',
        help_text=("Filter by ID containing value")
    )
    start_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='istartswith',
        help_text=("Filter by ID starting with value")
    )
    end_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iendswith',
        help_text=("Filter by ID ending with value"))
    ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='iexact',
        help_text=("Filter by exact TTN number (case-insensitive)"))
    cont_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='icontains',
        help_text=("Filter by TTN containing value (case-insensitive)"))
    start_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='istartswith',
        help_text=("Filter by TTN starting with value (case-insensitive)"))
    end_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='iendswith',
        help_text=("Filter by TTN ending with value (case-insensitive)"))
    recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='iexact')
    cont_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='icontains')
    start_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='istartswith')
    end_recipient = filters.CharFilter(
        field_name='recipient',
        lookup_expr='iendswith')
    date_calc = filters.DateFilter(
        field_name='date_calc',
        lookup_expr='iexact',
        help_text=("Filter by exact calculation date"))
    isnull_date_calc = filters.BooleanFilter(
        field_name='date_calc',
        lookup_expr='isnull',
        help_text=("Filter whether calculation date exists (true/false)"))

    class Meta:
        model = ClearanceInvoice
        fields = [
            'id',
            'cont_id',
            'start_id',
            'end_id',
            'ttn',
            'cont_ttn',
            'start_ttn',
            'end_ttn',
            'recipient',
            'cont_recipient',
            'start_recipient',
            'end_recipient',
            'date_calc',
            'isnull_date_calc',
        ]


class DocumentSezFilter(filters.FilterSet):
    """
    Filter for SEZ (Special Economic Zone) documents.

    Note: This appears to be a stub implementation - consider completing
    with proper model reference and field definitions.
    """
    product_id = filters.NumberFilter(
        field_name='product_id',
        lookup_expr='iexact'
    )
    cont_product_id = filters.NumberFilter(
        field_name='product_id',
        lookup_expr='icontains'
    )
    start_product_id = filters.NumberFilter(
        field_name='product_id',
        lookup_expr='istartswith'
    )
    end_product_id = filters.NumberFilter(
        field_name='product_id',
        lookup_expr='iendswith')
    exact_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iexact'
    )
    cont_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='icontains'
    )
    start_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='istartswith'
    )
    end_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iendswith'
    )
    declaration_number = filters.CharFilter(
        field_name='declaration_number',
        lookup_expr='iexact'
    )
    cont_declaration_number = filters.CharFilter(
        field_name='declaration_number',
        lookup_expr='icontains'
    )
    start_declaration_number = filters.CharFilter(
        field_name='declaration_number',
        lookup_expr='istartswith'
    )
    end_declaration_number = filters.CharFilter(
        field_name='declaration_number',
        lookup_expr='iendswith'
    )
    declaration_date = filters.CharFilter(
        field_name='declaration_date',
        lookup_expr='iexact'
    )
    cont_declaration_date = filters.CharFilter(
        field_name='declaration_date',
        lookup_expr='icontains'
    )
    start_declaration_date = filters.CharFilter(
        field_name='declaration_date',
        lookup_expr='istartswith'
    )
    end_declaration_date = filters.CharFilter(
        field_name='declaration_date',
        lookup_expr='iendswith'
    )
    amount = filters.NumberFilter(
        field_name='amount',
        lookup_expr='iexact'
    )
    cont_amount = filters.NumberFilter(
        field_name='amount',
        lookup_expr='icontains'
    )
    start_amount = filters.NumberFilter(
        field_name='amount',
        lookup_expr='istartswith'
    )
    end_amount = filters.NumberFilter(
        field_name='amount',
        lookup_expr='iendswith'
    )
    unit = filters.CharFilter(
        field_name='unit',
        lookup_expr='iexact'
    )
    cont_unit = filters.CharFilter(
        field_name='unit',
        lookup_expr='icontains'
    )
    start_unit = filters.CharFilter(
        field_name='unit',
        lookup_expr='istartswith'
    )
    end_unit = filters.CharFilter(
        field_name='unit',
        lookup_expr='iendswith'
    )
    cost = filters.NumberFilter(
        field_name='cost',
        lookup_expr='iexact'
    )
    cont_cost = filters.NumberFilter(
        field_name='cost',
        lookup_expr='icontains'
    )
    start_cost = filters.NumberFilter(
        field_name='cost',
        lookup_expr='istartswith'
    )
    end_cost = filters.NumberFilter(
        field_name='cost',
        lookup_expr='iendswith'
    )


class InnerTTNFilter(filters.FilterSet):
    start_uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='istartswith'
    )
    end_uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='iendswith'
    )
    cont_uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='icontains'
    )
    date = filters.DateFilter(
        field_name='date',
        lookup_expr='icontains'
    )
    start_notice = filters.CharFilter(
        field_name='notice',
        lookup_expr='istartswith'
    )
    end_notice = filters.CharFilter(
        field_name='notice',
        lookup_expr='iendswith'
    )
    cont_notice = filters.CharFilter(
        field_name='notice',
        lookup_expr='icontains'
    )
    noitce = filters.CharFilter(
        field_name='notice',
        lookup_expr='iexact'
    )
    quantity = filters.NumberFilter(method='filter_quantity')
    price = filters.NumberFilter(method='filter_price')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('uuid', 'uuid'),
            ('date', 'date'),
        ),
    )

    class Meta:
        model = InnerTTN
        fields = [
            'id',
            'uuid',
            'start_uuid',
            'end_uuid',
            'cont_uuid',
            'date',
            'start_notice',
            'end_notice',
            'cont_notice',
            'notice',
        ]

    def filter_quantity(self, queryset, name, value):
        return queryset.filter(innerttnitems__quantity__exact=value).distinct()

    def filter_price(self, queryset, name, value):
        return queryset.filter(innerttnitems__price_pcs__exact=value).distinct()
