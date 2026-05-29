from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.sreport.models import WarehouseMonthModelCount
from apps.sreport.serializers.warehouse_models_month_count import WarehouseModelMonthCountSerializer


@extend_schema(tags=['WarehouseReport'])
@extend_schema_view(
    get=extend_schema(
        description="Permission: IsAuthenticated",
        summary="Get count of models in warehouse per month",
    ))
class WarehouseModelMonthCount(ListAPIView):
    queryset = WarehouseMonthModelCount.objects.all()
    serializer_class = WarehouseModelMonthCountSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'model_name': ['iexact'],
    }
