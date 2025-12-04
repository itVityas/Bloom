from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse)
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from num2words import num2words

from apps.sez.models import InnerTTN, InnerTTNItems
from apps.invoice.serializers.pdf_invoice import PDFInvoiceSerializer
from apps.sez.permissions import ClearanceInvoicePermission
from apps.omega.models import OBJ_ATTR_VALUES_1000004


@extend_schema(tags=['ReportPDF'])
@extend_schema_view(
    get=extend_schema(
        summary='Generate invoice ttn (Счет фактура) pdf ',
        description='Permission: admin, stz_reader, stz, ttn',
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Wrong request"),
        }
    ),
)
class InvoiceTTNToPDFView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = PDFInvoiceSerializer
    queryset = InnerTTN.objects.all()

    def get(self, request, pk):
        ttn = InnerTTN.objects.filter(id=pk).first()
        if not ttn:
            return None
        items = InnerTTNItems.objects.filter(inner_ttn=ttn)

        quantity = 0
        price = 0
        weight = 0
        full_price = 0
        weight_gross = 0
        for item in items:
            short_name = item.model_name.short_name if item.model_name.short_name else item.model_name.name
            omega_obj = OBJ_ATTR_VALUES_1000004.objects.using('oracle_db').filter(
                A_3607=short_name).first()
            item.full_name = omega_obj.А_3173 if omega_obj else item.model_name.name
            quantity += item.quantity
            item.price = item.price_pcs * item.quantity
            price += item.price
            weight += item.weight * item.quantity
            weight_gross += item.weight_brutto * item.quantity
            item.nds_sum = price * item.nds / 100
            item.full_price = item.nds_sum + item.price
            full_price += item.full_price

        coin = int((full_price % 1) * 100)
        rub = int(full_price)
        rub_text = num2words(rub, lang='ru')
        weight_text = num2words(int(weight*1000), lang='ru')

        context = {
            "date": ttn.date.strftime("%d.%m.%Y"),
            "ttn": ttn,
            "items": items,
            "quantity": quantity,
            "price": price,
            "full_price": full_price,
            "weight": weight,
            "coin": coin,
            "rub_text": rub_text,
            "weight_text": weight_text,
            "weight_gross": weight_gross,
        }

        html_message = render_to_string(
            "invoicettn.html",
            context,
        )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'inner_ttn_{ttn.id}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        if not file_path:
            return HttpResponse('Не удалось сформировать PDF файл', status=400)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
