import django_filters as filters
from apps.declaration.models import Declaration


class DeclarationFilter(filters.FilterSet):
    declaration_number = filters.CharFilter(field_name='declaration_number', lookup_expr='iexact')
    start_declaration_number = filters.CharFilter(field_name='declaration_number', lookup_expr='istartswith')
    end_declaration_number = filters.CharFilter(field_name='declaration_number', lookup_expr='iendswith')
    cont_declaration_number = filters.CharFilter(field_name='declaration_number', lookup_expr='icontains')
    item_count = filters.NumberFilter(field_name='items__count', lookup_expr='exact')
    sender = filters.CharFilter(field_name='sender', lookup_expr='iexact')
    start_sender = filters.CharFilter(field_name='sender', lookup_expr='istartswith')
    end_sender = filters.CharFilter(field_name='sender', lookup_expr='iendswith')
    cont_sender = filters.CharFilter(field_name='sender', lookup_expr='icontains')
    outgoing_number = filters.CharFilter(field_name='outgoing_number', lookup_expr='iexact')
    start_outgoing_number = filters.CharFilter(field_name='outgoing_number', lookup_expr='istartswith')
    end_outgoing_number = filters.CharFilter(field_name='outgoing_number', lookup_expr='iendswith')
    cont_outgoing_number = filters.CharFilter(field_name='outgoing_number', lookup_expr='icontains')
    declaration_date = filters.DateFilter(field_name='declaration_date', lookup_expr='exact')
    container = filters.CharFilter(method='filter_container')
    start_container = filters.CharFilter(method='filter_start_container')
    end_container = filters.CharFilter(method='filter_end_container')
    cont_container = filters.CharFilter(method='filter_cont_container')
    order = filters.CharFilter(method='filter_order')
    start_order = filters.CharFilter(method='filter_start_order')
    end_order = filters.CharFilter(method='filter_end_order')
    cont_order = filters.CharFilter(method='filter_cont_order')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('declaration_number', 'declaration_number'),
            ('sender', 'sender'),
            ('outgoing_number', 'outgoing_number'),
            ('declaration_date', 'declaration_date'),
        ),
    )

    class Meta:
        model = Declaration
        fields = [
            'container',
            'declaration_number',
            'start_declaration_number',
            'end_declaration_number',
            'cont_declaration_number',
            'item_count',
            'sender',
            'start_sender',
            'end_sender',
            'cont_sender',
            'outgoing_number',
            'start_outgoing_number',
            'end_outgoing_number',
            'cont_outgoing_number',
            'declaration_date',
            'container',
            'start_container',
            'end_container',
            'cont_container',
            'order',
            'start_order',
            'end_order',
            'cont_order',
        ]

    def filter_container(self, queryset, name, value):
        return queryset.filter(container__name__iexact=value).distinct()

    def filter_start_container(self, queryset, name, value):
        return queryset.filter(container__name__istartswith=value).distinct()

    def filter_end_container(self, queryset, name, value):
        return queryset.filter(container__name__iendswith=value).distinct()

    def filter_cont_container(self, queryset, name, value):
        return queryset.filter(container__name__icontains=value).distinct()

    def filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iexact=value).distinct()

    def filter_start_order(self, queryset, name, value):
        return queryset.filter(container__order__name__istartswith=value).distinct()

    def filter_end_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iendswith=value).distinct()

    def filter_cont_order(self, queryset, name, value):
        return queryset.filter(container__order__name__icontains=value).distinct()
