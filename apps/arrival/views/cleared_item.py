from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.arrival.models import ClearedItem
from apps.arrival.permissions import ClearedItemPermission
from apps.arrival.serializers.cleared_item import ClearedItemSerializer


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    get=extend_schema(
        summary='List all cleared items',
        description='Permission: admin, arrival_reader, cleared_item_writer',
    ),
    post=extend_schema(
        summary='Create a cleared item',
        description='Permission: admin, cleared_item_writer',
    ),
)
class ClearedItemListCreateAPIView(ListCreateAPIView):
    """
    List all cleared items or create a new cleared item.
    """
    permission_classes = (IsAuthenticated, ClearedItemPermission)
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve cleared item by ID',
        description='Permission: admin, arrival_reader, cleared_item_writer',
    ),
    put=extend_schema(
        summary='Update cleared item',
        description='Permission: admin, cleared_item_writer',
    ),
    patch=extend_schema(
        summary='Partial update cleared item',
        description='Permission: admin, cleared_item_writer',
    ),
    delete=extend_schema(
        summary='Delete cleared item',
        description='Permission: admin, cleared_item_writer',
    ),
)
class ClearedItemDetailedView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a cleared item.
    """
    permission_classes = (IsAuthenticated, ClearedItemPermission)
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()
