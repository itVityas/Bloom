from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.invoice.models import TrainDoc
from apps.invoice.serializers.invoice import InvoicePostSerializer, InvoiceGetSerializer
from apps.invoice.permissions import InvoicePermission


@extend_schema(tags=["InvoiceFile"])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of invoices',
        description="Permission: 'admin', 'arrival_reader', 'invoice_writer'"
    )
)
class InvoiceListAPIView(ListAPIView):
    """List all invoices."""
    queryset = TrainDoc.objects.all()
    serializer_class = InvoiceGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'filename', 'order']


@extend_schema(tags=["InvoiceFile"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new invoice',
        description="Permission: 'admin', 'invoice_writer'"
    )
)
class InvoiceCreateAPIView(CreateAPIView):
    """Create a new invoice."""
    queryset = TrainDoc.objects.all()
    serializer_class = InvoicePostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=["InvoiceFile"])
@extend_schema_view(
    get=extend_schema(
        summary='Get invoice by id',
        description="Permission: 'admin', 'arrival_reader'"
    )
)
class InvoiceRetrieveAPIView(RetrieveAPIView):
    """Get invoice by id."""
    queryset = TrainDoc.objects.all()
    serializer_class = InvoiceGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=["InvoiceFile"])
@extend_schema_view(
    get=extend_schema(
        summary='Get invoice by id',
        description="Permission: 'admin', 'arrival_reader', 'invoice_writer'"
    ),
    put=extend_schema(
        summary='Update invoice by id',
        description="Permission: 'admin', 'invoice_writer'"
    ),
    patch=extend_schema(
        summary='Update invoice by id',
        description="Permission: 'admin', 'invoice_writer'"
    ),
    delete=extend_schema(
        summary='Delete invoice by id',
        description="Permission: 'admin', 'invoice_writer'"
    )
)
class InvoiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Get, update, and delete invoice by id."""
    queryset = TrainDoc.objects.all()
    serializer_class = InvoicePostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
