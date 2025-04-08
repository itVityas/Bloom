from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.omega.models import VzNorm
from apps.omega.serializers.vz_norm import VzNormSerializer


class VzNormListAPIView(APIView):
    def get(self, request):
        queryset = VzNorm.objects.using('oracle_db').all()[:100]
        serializer = VzNormSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
