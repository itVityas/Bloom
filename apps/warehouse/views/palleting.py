from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.warehouse.models import Palleting
from apps.warehouse.serializers.palleting import (
    PalletingGetSerializer,
    PalletingPostSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Palleting'])
@extend_schema_view(
    get=extend_schema(
        summary='get list palleting',
        description='Permission: admin, warehouse, warehouse_writer',
    )
)
class PalletingListAPIView(ListAPIView):
    queryset = Palleting.objects.all()
    serializer_class = PalletingGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'pallet',]


@extend_schema(tags=['Palleting'])
@extend_schema_view(
    post=extend_schema(
        summary='create palleting',
        description='Permission: admin, warehouse_writer'
    )
)
class PalletingCreateAPIView(CreateAPIView):
    queryset = Palleting.objects.all()
    serializer_class = PalletingPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Palleting'])
@extend_schema_view(
    get=extend_schema(
        summary='get palleting',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
    put=extend_schema(
        summary='update palleting',
        description='Permission: admin, warehouse_writer'
    ),
    patch=extend_schema(
        summary='partial update palleting',
        description='Permission: admin, warehouse_writer'
    ),
    delete=extend_schema(
        summary='delete palleting',
        description='Permission: admin, warehouse_writer'
    )
)
class PalletingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Palleting.objects.all()
    serializer_class = PalletingGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Palleting'])
@extend_schema_view(
    get=extend_schema(
        summary='get palleting',
        description='Permission: admin, warehouse, warehouse_writer'
    ),
)
class PalletingRetrieveAPIView(RetrieveAPIView):
    queryset = Palleting.objects.all()
    serializer_class = PalletingGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
