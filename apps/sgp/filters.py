import django_filters as filters

from apps.sgp.models import ShipmentBans


class ShipmentBansFilter(filters.FilterSet):
    """
    Advanced filtering for ShipmentBans with support for:
    - Exact matches and partial matches (prefix/suffix/contains)
    - Related model filtering (models, production codes, colors)
    - Date range filtering
    - Case-insensitive text matching

    Includes custom filter methods for related model fields.
    """
    id = filters.NumberFilter(
        field_name='id',
        lookup_expr='exact',
        help_text=("Filter by exact ID match"),)
    is_active = filters.BooleanFilter(
        field_name='is_active',
        lookup_expr='exact',
        help_text=("Filter by active status (true/false)"))
    barcode = filters.CharFilter(
        field_name='barcode',
        lookup_expr='iexact',
        help_text=("Exact barcode match (case-insensitive)"))
    start_barcode = filters.CharFilter(
        field_name='barcode',
        lookup_expr='istartswith',
        help_text=("Barcode starts with (case-insensitive)"))
    end_barcode = filters.CharFilter(
        field_name='barcode',
        lookup_expr='iendswith',
        help_text=("Barcode ends with (case-insensitive)"))
    cont_barcode = filters.CharFilter(
        field_name='barcode',
        lookup_expr='icontains',
        help_text=("Barcode contains (case-insensitive)"))
    pakaging_date_from = filters.DateFilter(
        field_name='pakaging_date_from',
        lookup_expr='exact',
        help_text=("Packaging date is on or after this date"))
    pakaging_date_to = filters.DateFilter(
        field_name='pakaging_date_to',
        lookup_expr='exact',
        help_text=("Packaging date is on or before this date"))
    model = filters.CharFilter(
        method='filter_model',
        help_text=("Exact model short name match"))
    start_model = filters.CharFilter(
        method='filter_start_model',
        help_text=("Model short name starts with"))
    end_model = filters.CharFilter(
        method='filter_end_model',
        help_text=("Model short name ends with"))
    cont_model = filters.CharFilter(
        method='filter_cont_model',
        help_text=("Model short name contains"))
    production = filters.CharFilter(
        method='filter_production',
        help_text=("Exact production code name match"))
    start_production = filters.CharFilter(
        method='filter_start_production',
        help_text=("Production code name starts with"))
    end_production = filters.CharFilter(
        method='filter_end_production',
        help_text=("Production code name ends with"))
    cont_production = filters.CharFilter(
        method='filter_cont_production',
        help_text=("Production code name contains"))
    color = filters.CharFilter(
        method='filter_color',
        help_text=("Exact color code match"))
    start_color = filters.CharFilter(
        method='filter_start_color',
        help_text=("Color code starts with"))
    end_color = filters.CharFilter(
        method='filter_end_color',
        help_text=("Color code ends with"))
    cont_color = filters.CharFilter(
        method='filter_cont_color',
        help_text=("Color code contains"))

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
