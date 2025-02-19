from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from Bloom.paginator import StandartResultPaginator
from apps.arrival.models import Content
from apps.arrival.permissions import ContentPermission
from apps.arrival.serializers.content import ContentSerializer


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='List all contents',
        description='Permission: admin, arrival_reader, content_writer',
    ),
    post=extend_schema(
        summary='Create content',
        description='Permission: admin, content_writer',
    ),
)
class ContentListView(ListCreateAPIView):
    """
    View to list all Content instances or create a new one.
    """
    permission_classes = (IsAuthenticated, ContentPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='Detailed content',
        description='Permission: admin, arrival_reader, content_writer',
    ),
    put=extend_schema(
        summary='Full update content',
        description='Permission: admin, content_writer',
    ),
    patch=extend_schema(
        summary='Partial update content',
        description='Permission: admin, content_writer',
    ),
    delete=extend_schema(
        summary='Delete content',
        description='Permission: admin, content_writer',
    ),
)
class ContentDetailView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a Content instance.
    """
    permission_classes = (IsAuthenticated, ContentPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
