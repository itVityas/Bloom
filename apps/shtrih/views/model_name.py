from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import ModelNames
from apps.shtrih.serializers.model_name import ModelNamesSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class ModelNameListView(ListAPIView):
    queryset = ModelNames.objects.all()
    serializer_class = ModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'short_name')
