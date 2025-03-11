import django_filters
from apps.declaration.models import Declaration

class DeclarationFilter(django_filters.FilterSet):
    """
    Custom filter for the Declaration model.

    This filter set allows filtering by the 'container' field using a custom method.
    If the filter value for 'container' is the string "null" (case-insensitive),
    the queryset is filtered to include only declarations with no associated container.
    Otherwise, it attempts to convert the provided value into an integer (container ID)
    and filters the declarations by that container. If the conversion fails, the original
    queryset is returned unmodified.

    Attributes:
        container (django_filters.CharFilter): A custom filter for the 'container' field.
    """
    container = django_filters.CharFilter(method='filter_container')

    class Meta:
        model = Declaration
        fields = ['container', 'declaration_id']

    def filter_container(self, queryset, name, value):
        """
        Filters the queryset based on the 'container' filter value.

        Args:
            queryset (QuerySet): The initial queryset of Declaration objects.
            name (str): The name of the filter field (expected to be "container").
            value (str): The filter value passed in the request query parameter.

        Returns:
            QuerySet: The filtered queryset. If 'value' is "null" (case-insensitive),
            the queryset will include only declarations with no associated container.
            Otherwise, if 'value' can be converted to an integer, it is treated as a container ID
            and the queryset is filtered to include declarations with that container.
            If the conversion fails, the original queryset is returned unmodified.
        """
        if value.lower() == 'null':
            return queryset.filter(container__isnull=True)
        else:
            try:
                container_id = int(value)
                return queryset.filter(container=container_id)
            except ValueError:
                return queryset
