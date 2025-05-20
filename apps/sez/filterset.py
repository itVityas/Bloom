import django_filters as filters

from .models import ClearanceInvoice, InnerTTN


class ClearanceInvoiceFilter(filters.FilterSet):
    """
    Filter for ClearanceInvoice
    """
    id = filters.NumberFilter(
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
        lookup_expr='iendswith')
    ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='iexact')
    cont_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='icontains')
    start_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='istartswith')
    end_ttn = filters.CharFilter(
        field_name='ttn',
        lookup_expr='iendswith')
    series = filters.CharFilter(
        field_name='series',
        lookup_expr='iexact')
    cont_series = filters.CharFilter(
        field_name='series',
        lookup_expr='icontains')
    start_series = filters.CharFilter(
        field_name='series',
        lookup_expr='istartswith')
    end_series = filters.CharFilter(
        field_name='series',
        lookup_expr='iendswith')
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
    quantity_shipped = filters.NumberFilter(
        field_name='quantity_shipped',
        lookup_expr='iexact')
    cont_quantity_shipped = filters.NumberFilter(
        field_name='quantity_shipped',
        lookup_expr='icontains')
    start_quantity_shipped = filters.NumberFilter(
        field_name='quantity_shipped',
        lookup_expr='istartswith')
    end_quantity_shipped = filters.NumberFilter(
        field_name='quantity_shipped',
        lookup_expr='iendswith')
    date_calc = filters.DateFilter(
        field_name='date_calc',
        lookup_expr='iexact')
    isnull_date_calc = filters.BooleanFilter(
        field_name='date_calc',
        lookup_expr='isnull')

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
            'series',
            'cont_series',
            'start_series',
            'end_series',
            'recipient',
            'cont_recipient',
            'start_recipient',
            'end_recipient',
            'quantity_shipped',
            'cont_quantity_shipped',
            'start_quantity_shipped',
            'end_quantity_shipped',
            'date_calc',
            'isnull_date_calc',
        ]


class DocumentSezFilter(filters.FilterSet):
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
            'cont_uuid'
        ]
