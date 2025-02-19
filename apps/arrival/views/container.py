from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.arrival.models import Container
from apps.arrival.serializers.container import (
    ContainerFullSerializer, ContainerSetSerializer, ContainerAndDeclarationSerializer
)
from apps.arrival.permissions import ContainerPermission, ArrivalPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='List all containers',
        description='Permissions: isAdmin, isArrival, isContainer',
    ),
)
class ContainerListView(ListAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerFullSerializer
    queryset = Container.objects.all()
    pagination_class = StandartResultPaginator


@extend_schema(tags=['Containers'])
@extend_schema_view(
    post=extend_schema(
        summary='Create container',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
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
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
    patch=extend_schema(
        summary='Partial update container',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
    delete=extend_schema(
        summary='Delete container',
        description='Permissions: isAdmin, isArrival_writer, isContainer',
    ),
)
class ContainerUpdateView(UpdateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerSetSerializer
    queryset = Container.objects.all()


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='List all containers with declarations',
        description='Permissions: isArrivalReader, isArrivalWriter',
    ),
)
class ContainerAndDeclarationView(ListAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = ContainerAndDeclarationSerializer
    queryset = Container.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve container with declarations',
        description='Permissions: isArrivalReader, isArrivalWriter',
    ),
)
class ContainerAndDeclarationDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = ContainerAndDeclarationSerializer
    queryset = Container.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None
