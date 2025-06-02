from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.sgp.models import ShipmentBans
from apps.sgp.serializers.shipment_bans import ShipmentBansGetSerializer, ShipmentBansPostSerializer
from apps.sgp.permissions import SGPPermission
from apps.sgp.filters import ShipmentBansFilter


@extend_schema(tags=['ShipmentBans'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new shipment ban',
        description='Permission: admin, sgp',
    )
)
class ShipmentBansCreateView(CreateAPIView):
    """
    API endpoint for creating new shipment bans/restrictions.

    Required permissions: admin or sgp
    """
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
    """
    API endpoint for listing and filtering shipment bans.

    Required permissions: admin, sgp, or sgp_reader
    """
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansGetSerializer
    permission_classes = (IsAuthenticated, SGPPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ShipmentBansFilter


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
    """
    API endpoint for retrieving, updating, and deleting shipment bans.

    Supports:
    - GET: Retrieve full details
    - PUT: Full update
    - PATCH: Partial update
    - DELETE: Remove ban

    Required permissions:
    - GET: admin, sgp, or sgp_reader
    - PUT/PATCH/DELETE: admin or sgp
    """
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
    """
    API endpoint for retrieving complete shipment ban information with all related data.

    Required permissions: admin, sgp, or sgp_reader
    """
    queryset = ShipmentBans.objects.all()
    serializer_class = ShipmentBansGetSerializer
    permission_classes = (IsAuthenticated, SGPPermission)
