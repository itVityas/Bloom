import django_filters as filters

from apps.sgp.models import ShipmentBans


class ShipmentBansFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    barcode = filters.CharFilter(field_name='barcode', lookup_expr='iexact')
    start_barcode = filters.CharFilter(field_name='barcode', lookup_expr='istartswith')
    end_barcode = filters.CharFilter(field_name='barcode', lookup_expr='iendswith')
    cont_barcode = filters.CharFilter(field_name='barcode', lookup_expr='icontains')
    pakaging_date_from = filters.DateFilter(field_name='pakaging_date_from', lookup_expr='exact')
    pakaging_date_to = filters.DateFilter(field_name='pakaging_date_to', lookup_expr='exact')
    model = filters.CharFilter(method='filter_model')
    start_model = filters.CharFilter(method='filter_start_model')
    end_model = filters.CharFilter(method='filter_end_model')
    cont_model = filters.CharFilter(method='filter_cont_model')
    production = filters.CharFilter(method='filter_production')
    start_production = filters.CharFilter(method='filter_start_production')
    end_production = filters.CharFilter(method='filter_end_production')
    cont_production = filters.CharFilter(method='filter_cont_production')
    color = filters.CharFilter(method='filter_color')
    start_color = filters.CharFilter(method='filter_start_color')
    end_color = filters.CharFilter(method='filter_end_color')
    cont_color = filters.CharFilter(method='filter_cont_color')

    class Meta:
        model = ShipmentBans
        fields = [
            'id',
            'is_active',
            'barcode',
            'start_barcode',
            'end_barcode',
            'cont_barcode',
            'pakaging_date_to',
            'pakaging_date_from',
            'model',
            'start_model',
            'end_model',
            'cont_model',
            'production',
            'start_production',
            'end_production',
            'cont_production',
            'color',
            'start_color',
            'end_color',
            'cont_color',
        ]

    def filter_model(self, queryset, name, value):
        return queryset.filter(model_name_id__short_name=value)

    def filter_start_model(self, queryset, name, value):
        return queryset.filter(model_name_id__short_name__istartswith=value)

    def filter_end_model(self, queryset, name, value):
        return queryset.filter(model_name_id__short_name__iendswith=value)

    def filter_cont_model(self, queryset, name, value):
        return queryset.filter(model_name_id__short_name__icontains=value)

    def filter_production(self, queryset, name, value):
        return queryset.filter(production_code_id__name=value)

    def filter_start_production(self, queryset, name, value):
        return queryset.filter(production_code_id__name__istartswith=value)

    def filter_end_production(self, queryset, name, value):
        return queryset.filter(production_code_id__name__iendswith=value)

    def filter_cont_production(self, queryset, name, value):
        return queryset.filter(production_code_id__name__icontains=value)

    def filter_color(self, queryset, name, value):
        return queryset.filter(color_id__color_code=value)

    def filter_start_color(self, queryset, name, value):
        return queryset.filter(color_id__color_code__istartswith=value)

    def filter_end_color(self, queryset, name, value):
        return queryset.filter(color_id__color_code__iendswith=value)

    def filter_cont_color(self, queryset, name, value):
        return queryset.filter(color_id__color_code__icontains=value)
