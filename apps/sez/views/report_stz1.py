from datetime import datetime

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.declaration.models import DeclaredItem
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
    permission_classes = (IsAuthenticated, STZPermission)
    seriaziler_class = DocumentRequestSerializer

    def post(self, request):
        ttn = request.data.get('ttn', None)
        document = request.data.get('document', None)
        if not ttn or not document:
            return HttpResponse("Missing required parameters", status=400)

        declaration = DeclaredItem.objects.select_related(
            'declaration').all().order_by('declaration')

        context = {
            "declarations": declaration,
            "ttn": ttn,
            "ttn_date": "13.03.2025",
            "document": document,
            "year": datetime.now().year,
            }

        html_message = render_to_string(
                "stz1.html",
                context,
            )
        font_config = FontConfiguration()

        file_path = 'tmp/' + f'{ttn}_{document}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
