from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.sgp.models import ShipmentBans
from apps.sgp.serializers.shipment_bans import ShipmentBansGetSerializer, ShipmentBansPostSerializer
from apps.sgp.permissions import SGPPermission


@extend_schema(tags=['ShipmentBans'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new shipment ban',
        description='Permission: admin, sgp',
    )
)
class ShipmentBansCreateView(CreateAPIView):
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansPostSerializer
    permission_classes = (IsAuthenticated, SGPPermission)


@extend_schema(tags=['ShipmentBans'])
@extend_schema_view(
    get=extend_schema(
        summary='List all shipment bans',
        description='Permission: admin, sgp, sgp_reader',
    )
)
class ShipmentBansListView(ListAPIView):
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansGetSerializer
    permission_classes = (IsAuthenticated, SGPPermission)


@extend_schema(tags=['ShipmentBans'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve a shipment ban',
        description='Permission: admin, sgp, sgp_reader',
    ),
    put=extend_schema(
        summary='Update a shipment ban',
        description='Permission: admin, sgp',
    ),
    patch=extend_schema(
        summary='Partial update a shipment ban partial',
        description='Permission: admin, sgp',
    ),
    delete=extend_schema(
        summary='Delete a shipment ban',
        description='Permission: admin, sgp',
    ),
)
class ShipmentBansRUDView(RetrieveUpdateDestroyAPIView):
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansPostSerializer
    permission_classes = (IsAuthenticated, SGPPermission)


@extend_schema(tags=['ShipmentBans'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve a full shipment ban',
        description='Permission: admin, sgp, sgp_reader',
    ),
)
class ShipmentBansGetView(RetrieveAPIView):
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansGetSerializer
    permission_classes = (IsAuthenticated, SGPPermission)
