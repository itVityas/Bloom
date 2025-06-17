import django_filters as filters

from apps.invoice.models import InvoiceContainer


class InvoiceContainerFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="iexact")
    number = filters.CharFilter(field_name="number", lookup_expr="iexact")
    start_number = filters.CharFilter(field_name="number", lookup_expr="istartswith")
    end_number = filters.CharFilter(field_name="number", lookup_expr="iendswith")
    cont_number = filters.CharFilter(field_name="number", lookup_expr="icontains")
    container = filters.CharFilter(method='filter_container')
    start_container = filters.CharFilter(method='start_filter_container')
    end_container = filters.CharFilter(method='end_filter_container')
    cont_container = filters.CharFilter(method='cont_filter_container')
    order = filters.CharFilter(method='filter_order')
    start_order = filters.CharFilter(method='start_filter_order')
    end_order = filters.CharFilter(method='end_filter_order')
    cont_order = filters.CharFilter(method='cont_filter_order')

    class Meta:
        model = InvoiceContainer
        fields = [
            'id',
            'number',
            'start_number',
            'end_number',
            'cont_number',
            'container',
            'start_container',
            'end_container',
            'cont_container',
            'order',
            'start_order',
            'end_order',
            'cont_order'
        ]

    def filter_container(self, queryset, name, value):
        return queryset.filter(container__name__iexact=value)

    def start_filter_container(self, queryset, name, value):
        return queryset.filter(container__name__istartswith=value)

    def end_filter_container(self, queryset, name, value):
        return queryset.filter(container__name__iendswith=value)

    def cont_filter_container(self, queryset, name, value):
        return queryset.filter(container__name__icontains=value)

    def filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iexact=value)

    def start_filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__istartswith=value)

    def end_filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__iendswith=value)

    def cont_filter_order(self, queryset, name, value):
        return queryset.filter(container__order__name__icontains=value)
