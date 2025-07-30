from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from apps.warehouse.models import Shipment
from apps.warehouse.serializers.shipment import (
    ShipmentGetSerializer,
    ShipmentPostSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import ShipmentFilter


@extend_schema(tags=["Shipments"])
@extend_schema_view(
    post=extend_schema(
        summary='Create shipment',
        description='Permission: admin, warehouse_writer',
    ),
)
class ShipmentCreateAPIView(CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get all shipments',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class ShipmentListAPIView(ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShipmentFilter
    pagination_class = StandartResultPaginator


@extend_schema(tags=["Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get shipment',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update shipment',
        description='Permission: admin, warehouse_writer',
    ),
    patch=extend_schema(
        summary='Update shipment',
        description='Permission: admin, warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete shipment',
        description='Permission: admin, warehouse_writer',
    ),
)
class ShipmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["Shipments"])
@extend_schema_view(
    get=extend_schema(
        summary='Get shipment',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class ShipmentRetrieveAPIView(RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
