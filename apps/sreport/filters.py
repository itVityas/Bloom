import django_filters as filters
from django.db.models import Sum

from apps.sreport.models import ReportStorage
from apps.shtrih.models import ModelNames


class ReportStorageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    start_name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    end_name = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    cont_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    production_code = filters.NumberFilter(method='filter_production_code')
    warehouse_id = filters.NumberFilter(method='filter_warehouse_id')

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
            'warehouse_id',
        ]

    def filter_production_code(self, queryset, name, value):
        model_names = ModelNames.objects.distinct().filter(
            models__production_code__code=value).values_list('id', flat=True)
        return queryset.filter(model_name_id__in=model_names)

    def filter_warehouse_id(self, queryset, name, value):
        if not value:
            return queryset.values(
                'model_name_id', 'name'
            ).annotate(
                total_uncleared=Sum('uncleared'),
                total_cleared=Sum('cleared'),
                total_simple=Sum('simple'),
                total_compensation=Sum('compensation')
            )
        return queryset.filter(warehouse_id=value)
