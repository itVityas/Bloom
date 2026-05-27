from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from django.db.models import Sum

from apps.warehouse.models import WarehouseAction
from apps.shtrih.models import ModelNames


@extend_schema(tags=['WarehouseReport'])
@extend_schema_view(
    get=extend_schema(
        summary='Get models count by warehouse action per date range',
        description='isAuthenticated',
        parameters=[
            OpenApiParameter(
                name='date_start',
                description='date_start',
                required=True,
                type=date
            ),
            OpenApiParameter(
                name='date_end',
                description='date_end',
                required=True,
                type=date
            )
        ],
        responses={
            200: OpenApiResponse(description='OK'),
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
        },
    )
)
class ModelsWarehouseActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_start = request.query_params.get('date_start')
        date_end = request.query_params.get('date_end')
        if not date_start or not date_end:
            return Response({'error': 'date_start and date_end are required'}, status=status.HTTP_400_BAD_REQUEST)

        warehouse_action = WarehouseAction.objects.all()
        rez_list = {}
        for action in warehouse_action:
            response_list = ModelNames.objects.filter(
                models__products__warehousedo__warehouse_ttn__warehouse_action_id=action.id,
                models__products__warehousedo__warehouse_ttn__date__range=(date_start, date_end)
            ).annotate(
                model_sum=Sum('models__products__warehousedo__quantity')
            ).order_by('name').values(
                'id',
                'name',
                'model_sum'
            )
            for i in response_list:
                buf = rez_list.get(i['name'])
                if buf:
                    rez_list[i['name']].append({
                        'id': i['id'],
                        'model_name': i['name'],
                        'quantity': int(i['model_sum']),
                        'action': action.name,
                        'action_id': action.id
                    })
                else:
                    rez_list[i['name']] = [{
                        'id': i['id'],
                        'model_name': i['name'],
                        'quantity': int(i['model_sum']),
                        'action': action.name,
                        'action_id': action.id
                    }]

        return Response(rez_list, status=status.HTTP_200_OK)
