from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.arrival.models import Order
from apps.arrival.serializers.order import (
    OrderSerializer, OrderListSerializer, OrderWithContainerSerializer)
from apps.arrival.permissions import ArrivalPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Orders'])
@extend_schema_view(
    post=extend_schema(
        summary='Создать заказ',
        description='isArrivalWriter',
    ),
)
class OrderCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех заказов',
        description='isArrivalReader, isArrivalWriter',
    ),
)
class OrderListView(ListAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить заказ по id',
        description='isArrivalReader, isArrivalWriter',
    ),
    put=extend_schema(
        summary='Обновить заказ',
        description='isArrivalWritter',
    ),
    patch=extend_schema(
        summary='Частичное обновление заказа',
        description='isArrivalWriter'
    ),
    delete=extend_schema(
        summary='Удалить заказ',
        description='isArrivalWriter',
    ),
)
class OrderDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех заказов c контейнерами',
        description='isArrivalReader, isArrivalWriter',
    ),
)
class OrderAndContainerListView(ListAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = OrderWithContainerSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Pаказ c контейнерами',
        description='isArrivalReader, isArrivalWriter',
    ),
)
class OrderAndContainerDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = OrderWithContainerSerializer
    queryset = Order.objects.all()