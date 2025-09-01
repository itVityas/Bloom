from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Bloom.paginator import StandartResultPaginator
from apps.arrival.models import Container, Order
from apps.arrival.permissions import ContainerPermission
from apps.arrival.serializers.container import (
    ContainerFullSerializer,
    ContainerSetSerializer,
    ContainerAndDeclarationSerializer,
    ContainerBindSerializer,
    ContainerAndContantSetSerializer,
    ContainerMassUpdateSerializer,
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container = serializer.save()
        return Response(ContainerAndDeclarationSerializer(container).data)


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
        summary='Retrieve detailed container',
        description='Permission: admin, arrival_reader, container_writer',
    ),

)
class ContainerDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerFullSerializer
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
    filterset_fields = ('name', 'lot')
    pagination_class = None


@extend_schema(tags=['Containers'])
@extend_schema_view(
    post=extend_schema(
        summary='Binds or unbinds given containers to/from the specified order.',
        description='Permission: admin, container_writer',
    ),
)
class BindContainersToOrderAPIView(APIView):
    """
    Binds given containers to the specified order. If 'order_id' is null, containers are unbound.
    """
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerBindSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get('order_id')
        container_ids = serializer.validated_data['container_ids']

        if order_id is not None:
            order = get_object_or_404(Order, pk=order_id)
        else:
            order = None

        updated_count = Container.objects.filter(id__in=container_ids).update(order=order)

        return Response({
            'status': f'{updated_count} container(s) updated.',
            'order_id': order_id,
            'container_ids': container_ids
        })


@extend_schema(tags=['Containers'])
@extend_schema_view(
    post=extend_schema(
        summary='Create container and content',
        description='Permission: admin, container_writer',
    ),
)
class ContainerAndContentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerAndContantSetSerializer
    queryset = Container.objects.all()


@extend_schema(tags=['Containers'])
@extend_schema_view(
    patch=extend_schema(
        summary='Partial update list container and content',
        description='Permission: admin, container_writer',
    ),
)
class ContainerListUpdateView(APIView):
    permission_classes = (IsAuthenticated, ContainerPermission)
    serializer_class = ContainerMassUpdateSerializer
    queryset = Container.objects.all()

    def patch(self, request):
        list_container = []
        for container_data in request.data:
            container_ser = ContainerMassUpdateSerializer(data=container_data)
            if container_ser.is_valid():
                container = Container.objects.filter(id=container_data.get('id', None)).first()
                container_ser.update(container, container_data)
                list_container.append(container)
        return Response(ContainerSetSerializer(list_container, many=True).data)
