from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.omega.serializers.compound import CompoundSerializer
from apps.shtrih.models import Models
from apps.omega.models import Stockobj
from apps.sez.clearance_workflow.calculate.omega_fetch import component_flat_list, fetch_analog_details


@extend_schema(tags=['Omega'])
@extend_schema_view(
    get=extend_schema(
        summary='Compound of model with analogs',
        description='''Permission: IsUser
        item_sign: обозначение в Омеге;
        item_unv: обозначение в 1C;
        nomsign: заводской код в Омеге;''',
        parameters=[
            OpenApiParameter(
                name='model_id',
                description='model_id.id',
                required=True,
                type=int,
            ),
        ],
    )
)
class CompoundOfModelWithAnalogs(APIView):
    """
    API endpoint that returns compound of model with analogs.

    Requires model_id query parameter.
    Returns paginated results using standard Bloom pagination format.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CompoundSerializer

    def get(self, request):
        model_id = request.query_params.get('model_id', None)
        if not model_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'model_id not fount'}
            )
        try:
            model = Models.objects.get(id=model_id)
            sign = f"{model.letter_part}{model.numeric_part}{model.execution_part or ''}"

            stockobjs = (
                Stockobj.objects
                .using('oracle_db')
                .filter(sign=sign, subtype=1)
                .values('sign', 'unvcode')
            ).first()

            flat_list = []
            if stockobjs:
                flat_list = component_flat_list(stockobjs['unvcode'], None, 1)

            for item in flat_list:
                item['analogs'] = fetch_analog_details(item['nomsign'])

            serializer = CompoundSerializer(flat_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
