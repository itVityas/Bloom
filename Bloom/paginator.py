from rest_framework.pagination import PageNumberPagination


class StandartResultPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'pagesize'
    max_page_size = 500
    reverse_param = 'reverse'

    def paginate_queryset(self, queryset, request, view=None):
        reverse_order = request.query_params.get(self.reverse_param, '').lower() == 'true'

        if reverse_order:
            queryset = queryset.reverse()

        return super().paginate_queryset(queryset, request, view)
