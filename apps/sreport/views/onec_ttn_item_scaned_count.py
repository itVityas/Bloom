from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.sreport.models import OneCTTNItemScanedCount
from Bloom.paginator import StandartResultPaginator
from apps.sreport.serializers.onec_ttn_item_scaned_count import OneCTTNItemScanedCountGetSerializer


@extend_schema(tags=['WarehouseReport'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC ttn item scaned count from sql view',
        description='Permission: IsAuthenticated',
    )
)
class OneCTTNItemScanedCountAPIView(ListAPIView):
    queryset = OneCTTNItemScanedCount.objects.all()
    serializer_class = OneCTTNItemScanedCountGetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'onec_ttn_item_id': ['exact'],
        'onec_ttn_number': ['iexact'],
        'onec_ttn_series': ['iexact'],
        'model_name_id': ['exact'],
        'warehouse_warehouse_id': ['exact'],
    }
