from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.arrival.models import Lot
from apps.arrival.serializers.lot import LotGetSerializer, LotPostSerializer
from apps.arrival.permissions import OrderPermission


@extend_schema(tags=['Lot'])
@extend_schema_view(
    get=extend_schema(
        summary='Get all lots',
        description='Permission: admin, arrival_reader, order_writer',
    ),
)
class LotListAPIView(ListAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotGetSerializer
    permission_classes = [IsAuthenticated, OrderPermission]


@extend_schema(tags=['Lot'])
@extend_schema_view(
    post=extend_schema(
        summary='Create lot',
        description='Permission: admin, arrival_writer',
    ),
)
class LotCreateAPIView(CreateAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotPostSerializer
    permission_classes = [IsAuthenticated, OrderPermission]


@extend_schema(tags=['Lot'])
@extend_schema_view(
    get=extend_schema(
        summary='Get lot by id',
        description='Permission: admin, arrival_reader, order_writer',
    ),
    put=extend_schema(
        summary='Update lot by id',
        description='Permission: admin, arrival_writer',
    ),
    patch=extend_schema(
        summary='Partially update lot by id',
        description='Permission: admin, arrival_writer',
    ),
    delete=extend_schema(
        summary='Delete lot by id',
        description='Permission: admin, arrival_writer',
    ),
)
class LotRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotPostSerializer
    permission_classes = [IsAuthenticated, OrderPermission]
