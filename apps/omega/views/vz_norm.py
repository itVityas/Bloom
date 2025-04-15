from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.omega.models import VzNorm
from apps.omega.serializers.vz_norm import VzNormSerializer


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='List all vz_norm connected by unvcode or ko_sing',
        description='Permission: admin, arrival_reader, omega_writer',
    ),
)
class VzNormListAPIView(APIView):
    """
    Get all vz_norm connected by unvcode or ko_sing.
    """
    def get(self, request):
        unvcode = request.query_params.get('unvcode')
        ko_sign = request.query_params.get('ko_sign')

        queryset = VzNorm.objects.using('oracle_db').all()

        if unvcode:
            queryset = queryset.filter(unvcode=unvcode)
        elif ko_sign:
            queryset = queryset.filter(ko_sign=ko_sign)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VzNormSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
