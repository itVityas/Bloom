from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.sgp.models import StorageLimits
from apps.sgp.serializers.storage_limits import StorageLimitsGetSerializer, StorageLimitsPostSerializer
from apps.sgp.permissions import SGPPermission


@extend_schema(tags=['StorageLimits'])
@extend_schema_view(
    get=extend_schema(
        summary='List all storage limits',
        description='Permission: admin, sgp_reader, sgp',
    )
)
class StorageLimitsListView(ListAPIView):
    queryset = StorageLimits.objects.all()
    serializer_class = StorageLimitsGetSerializer
    permission_classes = (IsAuthenticated, SGPPermission)


@extend_schema(tags=['StorageLimits'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a storage limit',
        description='Permission: admin, sgp',
    )
)
class StorageLimitsCreateView(CreateAPIView):
    queryset = StorageLimits.objects.all()
    serializer_class = StorageLimitsPostSerializer
    permission_classes = (IsAuthenticated, SGPPermission)


@extend_schema(tags=['StorageLimits'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a storage limit',
        description='Permission: admin, sgp_reader, sgp',
    ),
    put=extend_schema(
        summary='Update a storage limit',
        description='Permission: admin, sgp',
    ),
    patch=extend_schema(
        summary='Update a storage limit partial',
        description='Permission: admin, sgp',
    ),
    delete=extend_schema(
        summary='Delete a storage limit',
        description='Permission: admin, sgp',
    )
)
class StorageLimitsRUDView(RetrieveUpdateDestroyAPIView):
    queryset = StorageLimits.objects.all()
    serializer_class = StorageLimitsPostSerializer
    permission_classes = (IsAuthenticated, SGPPermission)
