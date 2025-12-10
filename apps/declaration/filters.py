import django_filters as filters
from apps.declaration.models import Declaration, DeclaredItem


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
    gifted = filters.BooleanFilter(field_name='gifted', lookup_expr='exact')
    container = filters.CharFilter(method='filter_container')
    start_container = filters.CharFilter(method='filter_start_container')
    end_container = filters.CharFilter(method='filter_end_container')
    cont_container = filters.CharFilter(method='filter_cont_container')
    order = filters.CharFilter(method='filter_order')
    start_order = filters.CharFilter(method='filter_start_order')
    end_order = filters.CharFilter(method='filter_end_order')
    cont_order = filters.CharFilter(method='filter_cont_order')
    order_id = filters.CharFilter(method='filter_order_id', lookup_expr='exact')
    is_use = filters.BooleanFilter(field_name='is_use', lookup_expr='exact')
    available = filters.NumberFilter(method='filter_available')
    item_name = filters.CharFilter(method='filter_item_name')
    start_item_name = filters.CharFilter(method='filter_start_item_name')
    end_item_name = filters.CharFilter(method='filter_end_item_name')
    cont_item_name = filters.CharFilter(method='filter_cont_item_name')
    is_completed = filters.BooleanFilter(field_name='is_completed', lookup_expr='exact')

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
            'gifted',
            'container',
            'start_container',
            'end_container',
            'cont_container',
            'order',
            'start_order',
            'end_order',
            'cont_order',
            'order_id',
            'is_use',
            'available',
            'item_name',
            'start_item_name',
            'end_item_name',
            'cont_item_name',
            'is_completed',
        ]

    def filter_container(self, queryset, name, value):
        val = value.strip().lower()
        if val == 'null':
            return queryset.filter(container__isnull=True)
        return queryset.filter(container__name__iexact=value).distinct()

    def filter_start_container(self, queryset, name, value):
        return queryset.filter(container__name__istartswith=value).distinct()

    def filter_end_container(self, queryset, name, value):
        return queryset.filter(container__name__iendswith=value).distinct()

    def filter_cont_container(self, queryset, name, value):
        return queryset.filter(container__name__icontains=value).distinct()

    def filter_order_id(self, queryset, name, value):
        if value == 'null' or value is None:
            return queryset.filter(container__order__isnull=True)
        return queryset.filter(container__order__id=value).distinct()

    def filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iexact=value).distinct()

    def filter_start_order(self, queryset, name, value):
        return queryset.filter(container__order__name__istartswith=value).distinct()

    def filter_end_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iendswith=value).distinct()

    def filter_cont_order(self, queryset, name, value):
        return queryset.filter(container__order__name__icontains=value).distinct()

    def filter_available(self, queryset, name, value):
        return queryset.filter(declared_items__available_quantity__gte=value).distinct()

    def filter_item_name(self, queryset, name, value):
        return queryset.filter(declared_items__name__iexact=value).distinct()

    def filter_start_item_name(self, queryset, name, value):
        return queryset.filter(declared_items__name__istartswith=value).distinct()

    def filter_end_item_name(self, queryset, name, value):
        return queryset.filter(declared_items__name__iendswith=value).distinct()

    def filter_cont_item_name(self, queryset, name, value):
        return queryset.filter(declared_items__name__icontains=value).distinct()


class DeclarationItemFilter(filters.FilterSet):
    declaration_item_id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    declaration_id = filters.NumberFilter(field_name='declaration__id', lookup_expr='exact')
    declaration_number = filters.CharFilter(
        field_name='declaration__declaration_number',
        lookup_expr='iexact')
    start_declaration_number = filters.CharFilter(
        field_name='declaration__declaration_number',
        lookup_expr='istartswith')
    end_declaration_number = filters.CharFilter(
        field_name='declaration__declaration_number',
        lookup_expr='iendswith')
    cont_declaration_number = filters.CharFilter(
        field_name='declaration__declaration_number',
        lookup_expr='icontains')
    available = filters.NumberFilter(field_name='available_quantity', lookup_expr='gte')
    ordinal_number = filters.NumberFilter(field_name='ordinal_number', lookup_expr='exact')

    class Meta:
        model = DeclaredItem
        fields = [
            'declaration_item_id',
            'declaration_id',
            'declaration_number',
            'start_declaration_number',
            'end_declaration_number',
            'cont_declaration_number',
            'available',
            'ordinal_number',
        ]
