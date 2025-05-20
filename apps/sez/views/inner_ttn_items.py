from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.sez.models import InnerTTNItems
from apps.sez.serializers.inner_ttn_item import InnerTTNItemsSerializer, InnerTTNItemsPostSerializer
from apps.sez.permissions import InnerTTNPermission


@extend_schema(tags=['InnerTTNItems'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of InnerTTNItems',
        description='Permission: admin, stz_reader, stz, ttn'
    ),
)
class InnerTTNItemsListView(ListAPIView):
    queryset = InnerTTNItems.objects.all()
    serializer_class = InnerTTNItemsSerializer
    permission_classes = [IsAuthenticated, InnerTTNPermission]


@extend_schema(tags=['InnerTTNItems'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new InnerTTNItem',
        description='Permission: admin, stz, ttn'
    )
)
class InnerTTNItemsCreateView(CreateAPIView):
    queryset = InnerTTNItems.objects.all()
    serializer_class = InnerTTNItemsPostSerializer
    permission_classes = [IsAuthenticated, InnerTTNPermission]


@extend_schema(tags=['InnerTTNItems'])
@extend_schema_view(
    get=extend_schema(
        summary='Get InnerTTNItem by id',
        description='Permission: admin, stz_reader, stz, ttn'
    ),
    put=extend_schema(
        summary='Update InnerTTNItem by id',
        description='Permission: admin, stz, ttn'
    ),
    patch=extend_schema(
        summary='Partially update InnerTTNItem by id',
        description='Permission: admin, stz, ttn'
    ),
    delete=extend_schema(
        summary='Delete InnerTTNItem by id',
        description='Permission: admin, stz, ttn'
    )
)
class InnerTTNItemsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = InnerTTNItems.objects.all()
    serializer_class = InnerTTNItemsPostSerializer
    permission_classes = [IsAuthenticated, InnerTTNPermission]
