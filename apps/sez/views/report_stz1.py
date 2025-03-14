from datetime import datetime

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from apps.declaration.models import Declaration, DeclaredItem
from apps.sez.permissions import STZPermission


@extend_schema(tags=['ReportPDF'])
@extend_schema_view(
    get=extend_schema(
        summary='Generate report STZ1 pdf ',
        description='Permission: admin, stz_reader',
        parameters=[
            OpenApiParameter(
                name='ttn',
                location=OpenApiParameter.QUERY,
                description='TTN number',
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name='document',
                location=OpenApiParameter.QUERY,
                description='Document number',
                required=True,
                type=int,
            ),
        ]
    ),
)
class ReportSTZ1View(GenericAPIView):
    permission_classes = (IsAuthenticated, STZPermission)
    queryset = Declaration.objects.all()

    def get(self, request):
        ttn = request.query_params.get('ttn', None)
        document = request.query_params.get('document', None)
        if not ttn or not document:
            return HttpResponse("Missing required parameters", status=400)

        declaration = Declaration.objects.all()
        declaration_items = DeclaredItem.objects.all()

        context = {
            "declarations": declaration,
            "declaration_items": declaration_items,
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

        file_path = 'tmp/' + f'{ttn}{document}.pdf'
        HTML(string=html_message).write_pdf(file_path, font_config=font_config)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
