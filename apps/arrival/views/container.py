from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Bloom.paginator import StandartResultPaginator
from apps.arrival.models import Container, Order
from apps.arrival.permissions import ContainerPermission
from apps.arrival.serializers.container import (
    ContainerFullSerializer, ContainerSetSerializer, ContainerAndDeclarationSerializer, DeclarationBindSerializer
)


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='List all containers',
        description='Permission: admin, arrival_reader, container_writer',
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
        description='Permission: admin, container_writer',
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
        description='Permission: admin, container_writer',
    ),
    patch=extend_schema(
        summary='Partial update container',
        description='Permission: admin, container_writer',
    ),
    delete=extend_schema(
        summary='Delete container',
        description='Permission: admin, container_writer',
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
        description='Permission: admin, arrival_reader, container_writer',
    ),
)
class ContainerAndDeclarationView(ListAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerAndDeclarationSerializer
    queryset = Container.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


@extend_schema(tags=['Containers'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve container with declarations',
        description='Permission: admin, arrival_reader, container_writer',
    ),
)
class ContainerAndDeclarationDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerAndDeclarationSerializer
    queryset = Container.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


@extend_schema(tags=['Containers'])
@extend_schema_view(
    post=extend_schema(
        summary='Binds given containers to the specified order.',
        description='Permission: admin, container_writer',
    ),
)
class BindContainersToOrderAPIView(APIView):
    """
    Binds given containers to the specified order.
    """
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = DeclarationBindSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        container_ids = serializer.validated_data['container_ids']

        order = get_object_or_404(Order, pk=order_id)

        updated_count = Container.objects.filter(id__in=container_ids).update(order=order)

        return Response({
            'status': f'{updated_count} container updated.',
            'order_id': order_id,
            'container_ids': container_ids
        })
