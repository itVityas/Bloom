from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.arrival.models import Container
from apps.arrival.serializers.container import (
    ContainerFullSerializer, ContainerSetSerializer)
from apps.arrival.permissions import ContainerPermission


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='List all containers',
        description='isAdmin, isArrival, isContainer',
    ),
)
class ContainerListView(ListAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerFullSerializer
    queryset = Container.objects.all()


@extend_schema(tags=['Containers'])
@extend_schema_view(
    post=extend_schema(
        summary='Create container',
        description='isAdmin, isArrival_writter, isContainer',
    ),
)
class ContainerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerSetSerializer
    queryset = Container.objects.all()


@extend_schema(tags=['Containers'])
@extend_schema_view(
    put=extend_schema(
        summary='Full update container',
        description='isAdmin, isArrival_writter, isContainer',
    ),
    patch=extend_schema(
        summary='Part update container',
        description='isAdmin, isArrival_writter, isContainer',
    ),
    delete=extend_schema(
        summary='Delete container',
        description='isAdmin, isArrival_writter, isContainer',
    ),
)
class ContainerUpdateView(UpdateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerSetSerializer
    queryset = Container.objects.all()
