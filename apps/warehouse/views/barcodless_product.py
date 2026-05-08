from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import BarcodlessProductsFilter
from apps.warehouse.models import BarcodlessProducts
from apps.warehouse.permissions import WarehousePermission
from apps.warehouse.serializers.barcodless_product import BarcodlessProductFullSerializer


@extend_schema(tags=['BarcodlessProduct'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of BarcodlessProducts',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class BarcodlessProductListAPIView(ListAPIView):
    """
    View for getting list of BarcodlessProducts
    """
    serializer_class = BarcodlessProductFullSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = BarcodlessProductsFilter
    queryset = BarcodlessProducts.objects.select_related('model_name', 'color', 'warehouse')
