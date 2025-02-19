from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.arrival.models import Content
from apps.arrival.serializers.content import ContentSerializer
from apps.arrival.permissions import ContainerPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='List all contents',
        description='Permissions: isAdmin, isArrival, isContainer',
    ),
    post=extend_schema(
        summary='Create content',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
)
class ContentListView(ListCreateAPIView):
    """
    View to list all Content instances or create a new one.
    """
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='Detailed content',
        description='Permissions: isAdmin, isArrival, isContainer',
    ),
    put=extend_schema(
        summary='Full update content',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
    patch=extend_schema(
        summary='Partial update content',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
    delete=extend_schema(
        summary='Delete content',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
)
class ContentDetailView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a Content instance.
    """
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
