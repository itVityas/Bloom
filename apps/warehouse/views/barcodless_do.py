from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from Bloom.paginator import StandartResultPaginator
from apps.warehouse.models import BarcodlessDo, BarcodlessProducts, WarehouseTTN
from apps.warehouse.permissions import WarehousePermission
from apps.warehouse.serializers.barcodless_do import (
    BarcodlessDoFullSerializer, BarcodlessDOUpdateSerializer, BarcodlessProductCreateSerializer)
from apps.warehouse.filters import BarcodlessDoFilter


@extend_schema(tags=['BarcodlessDo'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of BarcodlessDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
)
class BarcodlessDoListAPIView(ListAPIView):
    """
    View for getting list of BarcodlessDo
    """
    serializer_class = BarcodlessDoFullSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = BarcodlessDoFilter
    queryset = BarcodlessDo.objects.select_related('product', 'warehouse_ttn')


@extend_schema(tags=['BarcodlessDo'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new BarcodlessDo',
        description='''
        Permission: admin, warehouse_writer
        Создает barcodless_do, если нету создает warehouse_ttn, и создает/изменяет barcodless_products (количество)''',
    ),
)
class BarcodlessDoCreateAPIView(CreateAPIView):
    queryset = BarcodlessDo.objects.all()
    serializer_class = BarcodlessProductCreateSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]

    def post(self, request):
        try:
            serializer = BarcodlessProductCreateSerializer(data=request.data)
            if serializer.is_valid():
                barcodless_product = BarcodlessProducts.objects.filter(
                    model_name_id=serializer.validated_data['model_name_id'],
                    color_id=serializer.validated_data['color_id'],
                    warehouse_id=serializer.validated_data['warehouse_id']
                ).first()
                if not barcodless_product:
                    barcodless_product = BarcodlessProducts.objects.create(
                        model_name_id=serializer.validated_data['model_name_id'],
                        color_id=serializer.validated_data['color_id'],
                        warehouse_id=serializer.validated_data['warehouse_id'],
                        quantity=0
                    )
                warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=serializer.validated_data['ttn_number']).first()
                if not warehouse_ttn:
                    warehouse_ttn = WarehouseTTN.objects.create(
                        ttn_number=serializer.validated_data['ttn_number'],
                        is_close=False,
                        date=serializer.validated_data['date'],
                        warehouse_id=serializer.validated_data['warehouse_id'],
                        warehouse_action_id=serializer.validated_data['warehouse_action_id'],
                        user_id=request.user.id,
                        onec_ttn_id=serializer.validated_data['onec_ttn_id']
                    )
                barcodless_do = BarcodlessDo.objects.create(
                    product_id=barcodless_product.id,
                    warehouse_ttn=warehouse_ttn,
                    quantity=serializer.validated_data['quantity']
                )
                return Response(BarcodlessDoFullSerializer(barcodless_do).data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['BarcodlessDo'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a BarcodlessDo',
        description='Permission: admin, warehouse, warehouse_writer',
    ),
    put=extend_schema(
        summary='Update a BarcodlessDo',
        description='Permission: admin, warehouse_writer',
    ),
    patch=extend_schema(
        summary='partially update a BarcodlessDo',
        description='Permission: admin, warehouse_writer',
    ),
    delete=extend_schema(
        summary='Delete a BarcodlessDo',
        description='Permission: admin, warehouse_writer',
    )
)
class BarcodlessDoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BarcodlessDOUpdateSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    queryset = BarcodlessDo.objects.all()
