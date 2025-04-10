from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    RetrieveAPIView, ListAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.sez.models import ClearanceInvoice
from apps.sez.permissions import ClearanceInvoicePermission
from apps.sez.serializers.clearance_invoice import (
    ClearanceInvoiceSerializer, FullClearanceInvoiceSerializer)
from Bloom.paginator import StandartResultPaginator
from apps.sez.filterset import ClearanceInvoiceFilter


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='List all clearance invoices',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
    post=extend_schema(
        summary='Create a clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
)
class ClearanceInvoiceListCreateAPIView(ListCreateAPIView):
    """
    List all clearance invoices or create a new clearance invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve clearance invoice by ID',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
    put=extend_schema(
        summary='Update clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
    patch=extend_schema(
        summary='Partial update clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
    delete=extend_schema(
        summary='Delete clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
)
class ClearanceInvoiceDetailedView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a clearance invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Get full clearance invoice',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    )
)
class GetFullClearanceInvoiceView(RetrieveAPIView):
    """
    Get ClearanceInvoice + ClearanceInvoiceItem
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = FullClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='List all clearance invoices + items',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
)
class GetFullClearancesInvoiceListView(ListAPIView):
    """
    Get ClearanceInvoice + ClearanceInvoiceItem
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = FullClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend,]
    filterset_class = ClearanceInvoiceFilter
