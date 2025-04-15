from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.omega.models import VzNab
from apps.omega.serializers.vz_norm import VzNormSerializer


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Get all vz_norm connected by scp_unv or spc_sign.',
        description='Permission: admin, arrival_reader, omega_writer',
    ),
)
class VzNabListAPIView(APIView):
    def get(self, request):
        scp_unv = request.query_params.get('scp_unv')
        spc_sign = request.query_params.get('spc_sign')

        queryset = VzNab.objects.using('oracle_db').all()

        if scp_unv:
            queryset = queryset.filter(scp_unv=scp_unv)
        elif spc_sign:
            queryset = queryset.filter(scp_unv=spc_sign)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VzNormSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
