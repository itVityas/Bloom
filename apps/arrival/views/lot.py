from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.arrival.models import Lot, Container
from apps.arrival.serializers.lot import LotGetSerializer, LotPostSerializer
from apps.arrival.permissions import OrderPermission
from apps.invoice.models import InvoiceContainer


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
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['id', 'name', 'order']


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

    def delete(self, request, *args, **kwargs):
        containers = Container.objects.filter(lot=kwargs['pk'])
        InvoiceContainer.objects.filter(container__in=containers).update(sheet=None)
        return super().delete(request, *args, **kwargs)
