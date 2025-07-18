from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import WarehouseProductHistory
from apps.warehouse.serializers.warehouse_product_history import WarehouseProductHistoryGetSerializer
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import WarehouseProductHistoryFilter


@extend_schema(tags=['WarehouseProductHistory'])
@extend_schema_view(
    get=extend_schema(
        summary='List of WarehouseProductHistory',
        description='Retrieve a list of WarehouseProductHistory'
    )
)
class WarehouseProductHistoryListAPIView(ListAPIView):
    queryset = WarehouseProductHistory.objects.all()
    serializer_class = WarehouseProductHistoryGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseProductHistoryFilter
