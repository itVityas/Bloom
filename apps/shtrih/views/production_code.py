from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Production_codes
from apps.shtrih.serializers.production_code import ProductionCodeSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List production_code',
        description="description='Permission: admin, strih"
    )
)
class ProductionCodeListView(ListAPIView):
    permission_classes = (IsAuthenticated, StrihPermission)
    serializer_class = ProductionCodeSerializer
    queryset = Production_codes.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'name', 'nameplate']
