from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.sreport.models import OneCTTNItemScanedCount
from apps.onec.models import OneCTTNItem
from Bloom.paginator import StandartResultPaginator
from apps.sreport.serializers.onec_ttn_item_scaned_count import OneCTTNItemScanedCountGetSerializer
from rest_framework import status
from rest_framework.response import Response


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


@extend_schema(tags=['WarehouseReport'])
@extend_schema_view(
    get=extend_schema(
        summary='Get OneC ttn item scaned count from sql view',
        description='Permission: IsAuthenticated',
    )
)
class OneCTTNItemScanedCountFullAPIView(ListAPIView):
    queryset = OneCTTNItemScanedCount.objects.all()
    serializer_class = OneCTTNItemScanedCountGetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'onec_ttn_item_id': ['exact'],
        'onec_ttn_number': ['exact'],
        'onec_ttn_series': ['exact'],
        'model_name_id': ['exact'],
        'warehouse_warehouse_id': ['exact'],
    }

    def get(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            query_params = request.query_params.dict()
            allowed_fields = self.filterset_fields.keys()
            active_filters = {k: v for k, v in query_params.items() if k in allowed_fields}
            onec_items = OneCTTNItem.objects.select_related('onec_ttn', 'model_name').all()
            for key, value in active_filters.items():
                if key == 'warehouse_warehouse_id':
                    continue
                if key == 'onec_ttn_item_id':
                    onec_items = onec_items.filter(pk=value)
                if key == 'onec_ttn_number':
                    onec_items = onec_items.filter(onec_ttn__number=value)
                if key == 'onec_ttn_series':
                    onec_items = onec_items.filter(onec_ttn__series=value)
                if key == 'model_name_id':
                    onec_items = onec_items.filter(model_name__id=value)
            onec_rez = []
            onec_rez_ids = set()
            for i in queryset:
                onec_rez_ids.add(i.onec_ttn_item_id)
                onec_rez.append({
                    'onec_ttn_item_id': i.onec_ttn_item_id,
                    'onec_ttn_number': i.onec_ttn_number,
                    'onec_ttn_series': i.onec_ttn_series,
                    'model_name_id': i.model_name_id,
                    'full_name': i.full_name,
                    'color_id': i.color_id,
                    'color_code': i.color_code,
                    'count': i.count,
                    'warehouse_warehouse_id': i.warehouse_warehouse_id,
                    'warehouse_name': i.warehouse_name,
                    'scanned': i.scanned
                })
            for i in onec_items:
                if i.id in onec_rez_ids:
                    continue
                onec_rez.append({
                    'onec_ttn_item_id': i.id,
                    'onec_ttn_number': i.onec_ttn.number,
                    'onec_ttn_series': i.onec_ttn.series,
                    'model_name_id': i.model_name.id,
                    'full_name': i.model_name.name,
                    'color_id': None,
                    'color_code': None,
                    'count': i.count,
                    'warehouse_warehouse_id': None,
                    'warehouse_name': None,
                    'scanned': 0
                })

            return Response({'results': onec_rez}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
