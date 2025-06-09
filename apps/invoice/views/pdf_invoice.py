from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse
)

from apps.invoice.serializers.pdf_invoice import PDFInvoiceSerializer
from apps.invoice.models import TrainDoc, InvoiceContainer
from apps.arrival.models import Container


@extend_schema(tags=["ReportXLSX"])
@extend_schema_view(
    post=extend_schema(
        summary="Generate report",
        description="Permission: authenticated",
        request=PDFInvoiceSerializer,
        responses={
            200: OpenApiResponse(description="Report generated successfully"),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)
class ReportXLSXView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PDFInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice_container_id = serializer.validated_data.get("invoice_container_id")
            invoice_container = InvoiceContainer.objects.filter(id=invoice_container_id).first()
            if not invoice_container:
                return Response({"error": "Invoice container not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
