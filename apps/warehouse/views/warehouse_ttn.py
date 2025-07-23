from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse
)
from rest_framework.response import Response
from rest_framework import status

from apps.warehouse.models import WarehouseTTN
from apps.warehouse.serializers.warehouse_ttn import (
    WarehouseTTNGetSerializer,
    WarehouseTTNPostSerializer
)
from apps.warehouse.permissions import WarehousePermission
from Bloom.paginator import StandartResultPaginator
from apps.warehouse.filters import WarehouseTTNFilter


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get all WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class WarehouseTTNListAPIView(ListAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseTTNFilter


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class WarehouseTTNCreateAPIView(CreateAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a WarehouseTTN',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    patch=extend_schema(
        summary='partial update a WarehouseTTN',
        description='Permission: admin warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a WarehouseTTN',
        description='Permission: admin, warehouse_writer',
    )
)
class WarehouseTTNRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNPostSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=["WarehouseTTN"])
@extend_schema_view(
    get=extend_schema(
        summary='Get detailed WarehouseTTN by id',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class WarehouseTTNRetrieveAPIView(RetrieveAPIView):
    queryset = WarehouseTTN.objects.all()
    serializer_class = WarehouseTTNGetSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get latest WarehouseTTN by user_id',
        description='Permission: admin, warehouse, warehouse_writer',
        parameters=[
            OpenApiParameter(
                name='user_id',
                description='User ID',
                required=True,
                type=int
            )
        ],
        responses={
            200: WarehouseTTNGetSerializer,
            404: OpenApiResponse(description='WarehouseTTN not found')
        },
    ),
)
class WarehouseTTNByUserIdAPIView(APIView):
    permission_classes = [IsAuthenticated, WarehousePermission]
    serializer_class = WarehouseTTNGetSerializer

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
                )

        warehouse_ttn = WarehouseTTN.objects.filter(
            user_id=user_id,
            ).order_by('-create_at').first()
        if not warehouse_ttn:
            return Response(
                {'error': 'WarehouseProduct not found'},
                status=status.HTTP_404_NOT_FOUND)

        return Response(
                self.serializer_class(warehouse_ttn).data,
                status=status.HTTP_200_OK
            )
