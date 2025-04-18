import time

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse)
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.sez.serializers.document_sez import DocumentClearedItemSerializer
from apps.sez.models import ClearanceInvoice, ClearedItem
from apps.sez.filterset import DocumentSezFilter
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Sez_document'])
@extend_schema_view(
    get=extend_schema(
        summary='custom clearance',
        description='Permission: admin, stz_reader',
        responses={
            status.HTTP_200_OK: OpenApiResponse(description='ok'),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description='wrong data')
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
class CustomClearanceView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentClearedItemSerializer
    queryset = ClearedItem.objects.all()

    def get(self, request):
        clearanceinvoice_id = request.query_params.get('id', None)
        if not clearanceinvoice_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'id is required'}
            )

        cleranceinvoice = ClearanceInvoice.objects.filter(
            id=clearanceinvoice_id
        ).first()
        if not cleranceinvoice:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'clearanceinvoice not fount'}
            )

        # temporaly
        if not cleranceinvoice.cleared:
            time.sleep(5)
        cleranceinvoice.cleared = True
        cleranceinvoice.save()

        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=['Sez_document'])
@extend_schema_view(
    get=extend_schema(
        summary='a hz',
        description='Permission: admin, stz_reader',
        responses={
            status.HTTP_200_OK: DocumentClearedItemSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description='wrong data')
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
class DocumentSezView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentClearedItemSerializer
    queryset = ClearedItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DocumentSezFilter
    pagination_class = StandartResultPaginator

    def get(self, request):
        clearanceinvoice_id = request.query_params.get('id', None)
        if not clearanceinvoice_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'id is required'}
            )

        cleranceinvoice = ClearanceInvoice.objects.filter(
            id=clearanceinvoice_id
        ).first()
        if not cleranceinvoice:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'clearanceinvoice not fount'}
            )

        # temporaly
        if not cleranceinvoice.cleared:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={'error': 'clearanceinvoice not cleared'}
            )

        cleared_items = ClearedItem.objects.filter().order_by('id')

        # filtering from url
        filter_queryset = self.filter_queryset(cleared_items)

        # pagination
        page = self.paginate_queryset(filter_queryset)

        serializer = DocumentClearedItemSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
