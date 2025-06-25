from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse)
from django.http import HttpResponse

from apps.invoice.models import InvoiceContainer, TrainDoc
from apps.invoice.permissions import InvoicePermission
from apps.invoice.utils.exel_to_html import excel_sheet_to_html


@extend_schema(tags=['ReportPDF'])
@extend_schema_view(
    get=extend_schema(
        summary="Generate report invoice to pdf",
        description="Permission: 'admin', 'arrival_reader', 'invoice_writer'",
        parameters=[
            OpenApiParameter(
                name='invoice_id',
                type=int,
                description='Invoice id',
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(description="Report generated successfully"),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found"),
        },
    )
)
class InvoiceToPDFView(APIView):
    permission_classes = (IsAuthenticated, InvoicePermission)

    def get(self, request):
        invoice_id = request.query_params.get('invoice_id', None)
        if not invoice_id:
            return Response({"error": "Invoice id is required"}, status=status.HTTP_400_BAD_REQUEST)

        invoice = InvoiceContainer.objects.filter(id=invoice_id).first()
        if not invoice:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        traindoc = TrainDoc.objects.filter(lot=invoice.container.lot).first()
        if not traindoc:
            return Response({"error": "TrainDoc not found"}, status=status.HTTP_404_NOT_FOUND)

        html_file = 'tmp/invoice.html'
        rez = excel_sheet_to_html(traindoc.file.path, invoice.sheet, html_file, "exel.html")
        if rez is False:
            return Response({"error": "Error in excel_sheet_to_html"}, status=status.HTTP_400_BAD_REQUEST)

        document = open(html_file, 'rb')
        file_name = html_file.split('/')[1]
        response = HttpResponse(document, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
