from rest_framework.pagination import PageNumberPagination


class StandartResultPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'pagesize'
    max_page_size = 500
