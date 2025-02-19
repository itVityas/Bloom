from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from Bloom.paginator import StandartResultPaginator
from apps.arrival.models import Order
from apps.arrival.permissions import OrderPermission
from apps.arrival.serializers.order import (
    OrderSerializer, OrderListSerializer, OrderWithContainerSerializer
)


@extend_schema(tags=['Orders'])
@extend_schema_view(
    post=extend_schema(
        summary='Create order',
        description='Permission: admin, order_writer',
    ),
)
class OrderCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='List all orders',
        description='Permission: admin, arrival_reader, order_writer',
    ),
)
class OrderListView(ListAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve order by ID',
        description='Permission: admin, arrival_reader, order_writer',
    ),
    put=extend_schema(
        summary='Update order',
        description='Permission: admin, order_writer',
    ),
    patch=extend_schema(
        summary='Partial update order',
        description='Permission: admin, order_writer',
    ),
    delete=extend_schema(
        summary='Delete order',
        description='Permission: admin, order_writer',
    ),
)
class OrderDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='List all orders with containers',
        description='Permission: admin, arrival_reader, order_writer',
    ),
)
class OrderAndContainerListView(ListAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderWithContainerSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve order with containers',
        description='Permission: admin, arrival_reader, order_writer',
    ),
)
class OrderAndContainerDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderWithContainerSerializer
    queryset = Order.objects.all()
