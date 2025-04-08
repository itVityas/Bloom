import csv

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import StreamingHttpResponse


from apps.sez.permissions import STZPermission
from apps.sez.models import ClearedItem
from apps.shtrih.models import Products


@extend_schema(tags=['Sez_document'])
@extend_schema_view(
    get=extend_schema(
        summary='get barcode table excel file',
        description='Permission: admin, stz_reader, stz',
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="PDF file"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description='wrong parameter')
            },
        parameters=[
            OpenApiParameter(
                name='id',
                description='clearanceinvoice.id',
                type=int,
                location=OpenApiParameter.QUERY,
                required=True,
            )
        ]
    )
)
class BarcodeTable(APIView):
    permission_classes = (IsAuthenticated, STZPermission)

    def get(self, request):
        clearanceinvoice_id = request.query_params.get('id', None)
        if not clearanceinvoice_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})

        product_ids = ClearedItem.objects.filter(
            clearance_invoice__id=clearanceinvoice_id
        ).exclude(product_id__isnull=True).values_list('product_id', flat=True)

        products = Products.objects.filter(
            id__in=product_ids
        ).select_related('model__name').order_by('id')

        class Echo:
            def write(self, value):
                return value

        def generate_csv():
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_ALL)

            yield writer.writerow([
                'Product ID',
                'Model Short Name',
                'Barcode'
            ])

            for product in products:
                yield writer.writerow([
                    product.id,
                    product.model.name.short_name,
                    product.barcode
                ])

        response = StreamingHttpResponse(
            generate_csv(),
            content_type='text/csv; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="cleared_items_{clearanceinvoice_id}.csv"'
        return response
