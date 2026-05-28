from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from django.db.models import Sum

from apps.warehouse.models import Warehouse
from apps.shtrih.models import ModelNames


@extend_schema(tags=['WarehouseReport'])
@extend_schema_view(
    get=extend_schema(
        description="Permission: IsAuthenticated",
        summary="Get count of warehouse models",
        responses={
            200: OpenApiResponse(description="Success"),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        parameters=[
            OpenApiParameter(
                name='model_name_id',
                description='model_name_id',
                required=True,
                type=int
            ),
        ]
    ))
class WarehouseModelCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            model_name_id = request.query_params.get('model_name_id')
            model_name = ModelNames.objects.filter(id=model_name_id).first()
            if not model_name:
                return Response({'error': 'Model name not found'}, status=status.HTTP_404_NOT_FOUND)
            resp_query = Warehouse.objects.filter(
                warehousettn__warehousedo__product__model__name=model_name,
                warehousettn__warehousedo__product__available_quantity__gt=0
            ).annotate(total_sum=Sum('warehousettn__warehousedo__product__available_quantity')).values(
                'id', 'name', 'total_sum'
            )
            return Response({'model_name': model_name.name, 'result': resp_query}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
