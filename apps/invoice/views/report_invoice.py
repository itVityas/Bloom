from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework import status
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.invoice.permissions import InvoicePermission
from apps.invoice.models import Invoice, InvoiceItem


@extend_schema(tags=['Invoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Generate report invoice pdf ',
        description='Permission: admin, invoice_reader, invoice',
        parameters=[
            OpenApiParameter(
                name='invoice_id',
                location=OpenApiParameter.QUERY,
                description='invoice.id',
                required=True,
                type=int,
            ),
        ],
        responses={
            200: OpenApiResponse(description="PDF file with invoice data"),
            400: OpenApiResponse(description="Missing or invalid parameters"),
        }
    ),
)
class ReportPDFInvoice(APIView):
    """
    API View for generating PDF reports for invoices.

    This view generates a comprehensive PDF document containing:
    - Invoice header information
    - Line items grouped by product model
    - Subtotals by product model
    - Final totals including freight costs
    """
    permission_classes = (IsAuthenticated, InvoicePermission)

    def get(self, request):
        invoice_id = request.query_params.get('invoice_id', None)
        if not invoice_id:
            return HttpResponse('Missing required params', status=status.HTTP_400_BAD_REQUEST)
        invoice = Invoice.objects.filter(id=invoice_id).first()
        if not invoice:
            return HttpResponse('Invoice not found', status=status.HTTP_400_BAD_REQUEST)
        items = InvoiceItem.objects.filter(invoice=invoice)

        q_sum = 0
        n_sum = 0
        g_sum = 0
        amount = 0
        table = {}
        for item in items:
            model = table.get(item.model, None)
            if not model:
                model = {
                            "model": "",
                            "q_sum": 0,
                            "n_sum": 0,
                            "g_sum": 0,
                            "amount": 0,
                            "items": []
                        }
            model["model"] = item.model
            model["q_sum"] += item.quantity
            model["n_sum"] += item.net_weight
            model["g_sum"] += item.gross_weight
            model["amount"] += item.price_amount
            model["items"].append(item)
            q_sum += item.quantity
            n_sum += item.net_weight
            g_sum += item.gross_weight
            amount += item.price_amount
            table[item.model] = model

        total_sum = invoice.freight_cost + amount
        context = {
            'invoice': invoice,
            'table': table,
            'q_sum': q_sum,
            'n_sum': n_sum,
            'g_sum': g_sum,
            'amount': amount,
            'total_sum': total_sum
            }
        html_message = render_to_string(
                "invoice.html",
                context,
            )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'invoice{invoice_id}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
