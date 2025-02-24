import django_filters
from apps.arrival.models import Declaration

class DeclarationFilter(django_filters.FilterSet):
    container = django_filters.CharFilter(method='filter_container')

    class Meta:
        model = Declaration
        fields = ['container', 'declaration_id']

    def filter_container(self, queryset, name, value):
        if value.lower() == 'null':
            return queryset.filter(container__isnull=True)
        else:
            try:
                container_id = int(value)
                return queryset.filter(container=container_id)
            except ValueError:
                return queryset
