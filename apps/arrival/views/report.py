from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework import status

from apps.arrival.serializers.report import ListOrderSerializer
from apps.arrival.permissions import ArrivalPermission


@extend_schema(tags=['ReportCSV'])
@extend_schema_view(
    get=extend_schema(
        summary='Get Orders report in csv',
        description='Permission: admin, arrival_reader, order_writer',
        request=ListOrderSerializer,
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Missing required parameters"),
        }
    )
)
class ReportCSVView(APIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)

    def get(self, request):
        return ListOrderSerializer(data={'list': []}).data
