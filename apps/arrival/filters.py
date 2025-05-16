import django_filters as filters

from apps.arrival.models import Order


class OrderFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    start_name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    end_name = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    cont_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_container = filters.CharFilter(method='filter_name_container')
    start_name_container = filters.CharFilter(method='filter_start_name_container')
    end_name_container = filters.CharFilter(method='filter_end_name_container')
    cont_name_container = filters.CharFilter(method='filter_cont_name_container')
    declaration_number = filters.CharFilter(method='filter_declaration_number')
    start_declaration_number = filters.CharFilter(method='filter_start_declaration_number')
    end_declaration_number = filters.CharFilter(method='filter_end_declaration_number')
    cont_declaration_number = filters.CharFilter(method='filter_cont_declaration_number')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
        ),
        field_labels={
            'id': 'ID заказа',
            'name': 'Название заказа',
        }
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'start_name',
            'end_name',
            'cont_name',
            'name_container',
            'start_name_container',
            'end_name_container',
            'cont_name_container',
            'declaration_number',
            'start_declaration_number',
            'end_declaration_number',
            'cont_declaration_number',
        ]

    def filter_name_container(self, queryset, name, value):
        return queryset.filter(containers__name__iexact=value).distinct()

    def filter_start_name_container(self, queryset, name, value):
        return queryset.filter(container__name__istartswith=value).distinct()

    def filter_end_name_container(self, queryset, name, value):
        return queryset.filter(containers__name__iendswith=value).distinct()

    def filter_cont_name_container(self, queryset, name, value):
        return queryset.filter(containers__name__icontains=value).distinct()

    def filter_declaration_number(self, queryset, name, value):
        return queryset.filter(containers__declarations__declaration_number__exact=value).distinct()

    def filter_start_declaration_number(self, queryset, name, value):
        return queryset.filter(containers__declarations__declaration_number__istartswith=value).distinct()

    def filter_end_declaration_number(self, queryset, name, value):
        return queryset.filter(containers__declarations__declaration_number__iendswith=value).distinct()

    def filter_cont_declaration_number(self, queryset, name, value):
        return queryset.filter(containers__declarations__declaration_number__icontains=value).distinct()
