from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Colors
from apps.shtrih.serializers.color import ColorsSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get colors',
        description="description='Permission: admin, strih"
    )
)
class ColorsListView(ListAPIView):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'color_code', 'russian_title')
