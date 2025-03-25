from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse)
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.sez.permissions import STZPermission


@extend_schema(tags=['ReportPDF'])
@extend_schema_view(
    get=extend_schema(
        summary='Report for ClearanceInvoice pdf',
        description='Permission: admin, stz_reader',
        parameters=[
            OpenApiParameter(
                name='clearanceinvoice',
                location=OpenApiParameter.QUERY,
                description='ClearanceInvoice.id',
                required=True,
                type=int,
            ),
        ],
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Missing required parameters"),
        }
    )
)
class ReportClearanceInvoicePDFView(APIView):
    permission_classes = (IsAuthenticated, STZPermission)

    def get(self, request):
        clearance_invoice_id = request.query_params.get('clearanceinvoice')
        if not clearance_invoice_id:
            return HttpResponse('Missing parameters')

        context = {
            "clearance_invoice_id": clearance_invoice_id,
        }

        html_message = render_to_string(
                "clearanceinvoice.html",
                context,
            )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'{clearance_invoice_id}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
