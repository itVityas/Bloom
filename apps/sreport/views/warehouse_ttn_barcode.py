from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.sreport.models import WarehouseTTNBarcode
from apps.sreport.serializers.warehouse_ttn_barcode import WarehouseTTNBarcodeSerializer
from Bloom.paginator import StandartResultPaginator
from apps.sreport.filters import WarehouseTTNBarcodeFilter


@extend_schema(tags=['WarehouseTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a Barcode by 1c series and number',
        description='Permission: admin, warehouse, warehouse_writer',
        parameters=[
            OpenApiParameter(
                name='number',
                description='1C ttn number',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='series',
                description='1C ttn series',
                required=True,
                type=str
            )
        ],
    ),
)
class WarehouseTTNBarcodeListAPIView(ListAPIView):
    queryset = WarehouseTTNBarcode.objects.all()
    serializer_class = WarehouseTTNBarcodeSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseTTNBarcodeFilter

    def get(self, request):
        number = request.query_params.get('number')
        series = request.query_params.get('series')
        if not number or not series:
            return Response(
                {'error': 'number and series is required'},
                status=status.HTTP_400_BAD_REQUEST
                )
        query = self.filter_queryset(WarehouseTTNBarcode.objects.filter(onec_number=number, onec_series=series))
        page = self.paginate_queryset(query)
        return self.get_paginated_response(WarehouseTTNBarcodeSerializer(page, many=True).data)
