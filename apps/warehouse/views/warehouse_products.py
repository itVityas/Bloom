from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import WarehouseProduct
from apps.warehouse.serializers.warehouse_products import (
    WarehouseProductGetSerializer,
    WarehouseProductPostSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get list warehouse products',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class WarehouseProductListAPIView(ListAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'ttn_number', 'quantity']


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class WarehouseProductRetrieveAPIView(RetrieveAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    post=extend_schema(
        summary='create warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseProductCreateAPIView(CreateAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["WarehouseProduct"])
@extend_schema_view(
    get=extend_schema(
        summary='get warehouse product',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='partial update warehouse product',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete warehouse product',
        description='Permission: admin, warehouse_writer'
    )
)
class WarehouseProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
