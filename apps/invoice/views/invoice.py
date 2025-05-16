from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.invoice.models import Invoice
from apps.invoice.serializers.invoice import (
    InvoiceFullSerializer, InvoiceSerializer)
from apps.invoice.permissions import InvoicePermission
from Bloom.paginator import StandartResultPaginator
from apps.invoice.filters import InvoiceFilter


@extend_schema(tags=['Invoice'])
@extend_schema_view(
    get=extend_schema(
        summary='List all invoices (Full)',
        description='',
    ),
)
class InvoiceListAPIView(ListAPIView):
    """
    API view for full listing  Invoice instances with InvoiseItem.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceFullSerializer
    permission_classes = (IsAuthenticated, InvoicePermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InvoiceFilter
    ordering = ['-id']


@extend_schema(tags=['Invoice'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new invoice',
        description='',
    ),
)
class InvoiceCreateAPIView(CreateAPIView):
    """
    API view for create  Invoice instances .
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, InvoicePermission)


@extend_schema(tags=['Invoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a invoice',
        description='',
    ),
    put=extend_schema(
        summary='Update a invoice',
        description='',
    ),
    patch=extend_schema(
        summary='Partial update a invoice',
        description='',
    ),
    delete=extend_schema(
        summary='Delete a invoice',
        description='',
    )
)
class InvoiceDetailedAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrive, update, delete  Invoice instances .
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)
