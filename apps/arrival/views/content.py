from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.arrival.models import Content
from apps.arrival.serializers.content import ContentSerializer
from apps.arrival.permissions import ContainerPermission


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='List all contents',
        description='isAdmin, isArrival, isContainer',
    ),
    post=extend_schema(
        summary='Create content',
        description='isAdmin, isArrival_writter, isContainer',
    ),
)
class ContentListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()


@extend_schema(tags=['Contents'])
@extend_schema_view(
    get=extend_schema(
        summary='Detailed content',
        description='isAdmin, isArrival, isContainer',
    ),
    put=extend_schema(
        summary='Full update content',
        description='isAdmin, isArrival_writter, isContainer',
    ),
    patch=extend_schema(
        summary='Part update content',
        description='isAdmin, isArrival_writter, isContainer',
    ),
    delete=extend_schema(
        summary='Delete content',
        description='isAdmin, isArrival_writter, isContainer',
    ),
)
class ContentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
