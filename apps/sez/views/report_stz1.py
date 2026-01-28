from datetime import datetime

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.sez.models import ClearanceInvoice, ClearedItem
from apps.sez.permissions import STZPermission
from apps.sez.serializers.report_stz1 import DocumentRequestSerializer


@extend_schema(tags=['ReportPDF'])
@extend_schema_view(
    post=extend_schema(
        summary='Generate report STZ1 pdf ',
        description='Permission: admin, stz_reader',
        request=DocumentRequestSerializer,
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Missing required parameters"),
        }
    ),
)
class ReportSTZ1View(APIView):
    permission_classes = (IsAuthenticated,)
    seriaziler_class = DocumentRequestSerializer

    def post(self, request):
        invoices_id = request.data.get('ttn', None)

        if not invoices_id:
            return HttpResponse("Missing required parameters", status=400)

        temp_name = ''
        list_invoices = []
        for item in invoices_id:
            try:
                ids = item.get('name', None)
                list_invoices.append(int(ids))
                temp_name += ids
            except Exception:
                pass

        invoices = ClearanceInvoice.objects.filter(id__in=list_invoices)

        for i_invoice in invoices:
            cleared_items = ClearedItem.objects.filter(clearance_invoice_items__clearance_invoice=i_invoice) \
                .select_related('declared_item_id__declaration') \
                .order_by('declared_item_id__declaration__declaration_date')
            i_invoice.cleared_items = cleared_items

        context = {
            "invoices": invoices,
            "year": datetime.now().year,
            }

        html_message = render_to_string(
                "stz1.html",
                context,
            )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'{temp_name}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
