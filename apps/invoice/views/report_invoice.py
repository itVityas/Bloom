from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.invoice.permissions import InvoicePermission

@extend_schema(tags=['Invoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Generate report invoice pdf ',
        description='Permission: admin, invoice_reader, invoice',
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Missing required parameters"),
        }
    ),
)
class ReportPDFInvoice(APIView):
    permission_classes = (IsAuthenticated, InvoicePermission)

    def get(self, request):
        context = {
            'test': 'test'
            }
        html_message = render_to_string(
                "invoice.html",
                context,
            )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'invoice.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
