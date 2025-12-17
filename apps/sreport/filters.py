import django_filters as filters

from apps.sreport.models import ReportStorage
from apps.shtrih.models import ModelNames


class ReportStorageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    start_name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    end_name = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    cont_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    production_code = filters.NumberFilter(method='filter_production_code')

    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('uncleared', 'uncleared'),
            ('cleared', 'cleared'),
            ('simple', 'simple'),
            ('compensation', 'compensation'),
        ),
    )

    class Meta:
        model = ReportStorage
        fields = [
            'name',
            'start_name',
            'end_name',
            'cont_name',
            'production_code',
        ]

    def filter_production_code(self, queryset, name, value):
        model_names = ModelNames.objects.distinct().filter(
            models__production_code__code=value).values_list('id', flat=True)
        return queryset.filter(model_name_id__in=model_names)
