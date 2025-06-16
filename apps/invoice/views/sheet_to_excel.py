import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse
)
from django.http import HttpResponse

from apps.invoice.models import InvoiceContainer, TrainDoc
from apps.invoice.permissions import InvoicePermission
from apps.invoice.utils.sheet_to_excel import sheet_to_excel
from apps.arrival.models import Container
from apps.invoice.utils.check_excel import find_sheet


@extend_schema(tags=['ReportXLSX'])
@extend_schema_view(
    get=extend_schema(
        summary='Get invoice in pdf by invoice_container',
        description="Permission: 'admin', 'arrival_reader', 'invoice_reader'",
        parameters=[
            OpenApiParameter(
                name='invoice_container_id',
                description='invoice_container_id',
                required=True,
                type=int
            )
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
class InvoiceContainerSheetView(APIView):
    permission_classes = [IsAuthenticated, InvoicePermission]

    def get(self, request):
        invoice_container_id = request.query_params.get('invoice_container_id', None)
        if not invoice_container_id:
            return Response({'error': 'invoice_container_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        invoice_container = InvoiceContainer.objects.filter(id=invoice_container_id).first()
        if not invoice_container:
            return Response({'error': 'invoice_container not found'}, status=status.HTTP_404_NOT_FOUND)

        train_doc = TrainDoc.objects.filter(lot=invoice_container.container.lot).first()
        if not os.path.exists(train_doc.file.path):
            train_doc.file = None
            train_doc.save()
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)
        if not train_doc:
            return Response({'error': 'train_doc not found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = sheet_to_excel(train_doc.file.path, invoice_container.sheet)
        if not file_path:
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(
            document,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


@extend_schema(tags=['ReportXLSX'])
@extend_schema_view(
    get=extend_schema(
        summary='Get invoice in pdf by invoice_container',
        description="Permission: 'admin', 'arrival_reader', 'invoice_reader'",
        parameters=[
            OpenApiParameter(
                name='container',
                description='invoice_container_id',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='number',
                description='invoice_number',
                required=True,
                type=str
            )
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
class InvoiceByContainerNumberAPIView(APIView):
    permission_classes = [IsAuthenticated, InvoicePermission]

    def get(self, request):
        container_id = request.query_params.get('container', None)
        number = request.query_params.get('number', None)
        if not container_id or not number:
            return Response({'error': 'container and number are required'}, status=status.HTTP_400_BAD_REQUEST)

        container = Container.objects.filter(id=container_id).first()
        if not container:
            return Response({'error': 'container not found'}, status=status.HTTP_404_NOT_FOUND)

        train_doc = TrainDoc.objects.filter(lot=container.lot).first()
        if not train_doc:
            return Response({'error': 'train_doc not found'}, status=status.HTTP_404_NOT_FOUND)

        if not os.path.exists(train_doc.file.path):
            train_doc.file = None
            train_doc.save()
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)

        sheet = find_sheet(invoice_number=number, file=train_doc.file.path, container_name=container.name)
        if not sheet:
            return Response({'error': 'sheet not found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = sheet_to_excel(train_doc.file.path, sheet)
        if not file_path:
            return Response({'error': 'file_path not found'}, status=status.HTTP_404_NOT_FOUND)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(
            document,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
