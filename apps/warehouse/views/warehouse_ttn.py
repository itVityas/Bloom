from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.warehouse.models import WarehouseTTN
from apps.warehouse.serializers.warehouse_ttn import (
    WarehouseTTNSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import WarehouseTTNFilter


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get all WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    post=extend_schema(
        summary='Create a new WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class WarehouseTTNListCreateAPIView(ListCreateAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseTTNFilter


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    patch=extend_schema(
        summary='partial update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class WarehouseTTNRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
