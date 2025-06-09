from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.arrival.models import LotModel
from apps.arrival.serializers.lot_model import LotModelPostSerializer
from apps.arrival.permissions import OrderPermission


@extend_schema(tags=['LotModel'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new LotModel',
        description='Permission: admin, order_writer',
    ),
    get=extend_schema(
        summary='List all LotModels',
        description='Permission: admin, arrival_reader, order_writer',
    )
)
class LotModelListCreateAPIView(ListCreateAPIView):
    queryset = LotModel.objects.all()
    serializer_class = LotModelPostSerializer
    permission_classes = [IsAuthenticated, OrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lot', 'id']


@extend_schema(tags=['LotModel'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve a LotModel',
        description='Permission: admin, arrival_reader, order_writer',
    ),
    put=extend_schema(
        summary='Update a LotModel',
        description='Permission: admin, order_writer',
    ),
    patch=extend_schema(
        summary='Partial update a LotModel',
        description='Permission: admin, order_writer',
    ),
    delete=extend_schema(
        summary='Delete a LotModel',
        description='Permission: admin, order_writer',
    )
)
class LotModelRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LotModel.objects.all()
    serializer_class = LotModelPostSerializer
    permission_classes = [IsAuthenticated, OrderPermission]
