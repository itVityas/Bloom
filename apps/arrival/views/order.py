from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.arrival.models import Order
from apps.arrival.serializers.order import OrderSerializer
from apps.arrival.permissions import OrderPermission


@extend_schema(tags=['Orders'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех заказов',
        description='isArrivalReader, isArrivalWriter',
    ),
    post=extend_schema(
        summary='Создать заказ',
        description='isArrivalWriter',
    ),
)
class OrderListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


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
    permission_classes = (IsAuthenticated, OrderPermission)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
