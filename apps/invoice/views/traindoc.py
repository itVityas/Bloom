from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.invoice.models import TrainDoc
from apps.invoice.serializers.traindoc import TrainDocPostSerializer, TrainDocGetSerializer
from apps.invoice.permissions import InvoicePermission


@extend_schema(tags=["TrainDoc"])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of TrainDoc',
        description="Permission: 'admin', 'arrival_reader', 'invoice_writer'"
    )
)
class TrainDocListAPIView(ListAPIView):
    """List all TrainDoc."""
    queryset = TrainDoc.objects.all()
    serializer_class = TrainDocGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'filename', 'lot']


@extend_schema(tags=["TrainDoc"])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new TrainDoc',
        description="Permission: 'admin', 'invoice_writer'"
    )
)
class TrainDocCreateAPIView(CreateAPIView):
    """Create a new TrainDoc."""
    queryset = TrainDoc.objects.all()
    serializer_class = TrainDocPostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=["TrainDoc"])
@extend_schema_view(
    get=extend_schema(
        summary='Get TrainDoc by id',
        description="Permission: 'admin', 'arrival_reader'"
    )
)
class TrainDocRetrieveAPIView(RetrieveAPIView):
    """Get TrainDoc by id."""
    queryset = TrainDoc.objects.all()
    serializer_class = TrainDocGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=["TrainDoc"])
@extend_schema_view(
    get=extend_schema(
        summary='Get TrainDoc by id',
        description="Permission: 'admin', 'arrival_reader', 'invoice_writer'"
    ),
    put=extend_schema(
        summary='Update TrainDoc by id',
        description="Permission: 'admin', 'invoice_writer'"
    ),
    patch=extend_schema(
        summary='Update TrainDoc by id',
        description="Permission: 'admin', 'invoice_writer'"
    ),
    delete=extend_schema(
        summary='Delete inTrainDocoice by id',
        description="Permission: 'admin', 'invoice_writer'"
    )
)
class TrainDocRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Get, update, and delete TrainDoc by id."""
    queryset = TrainDoc.objects.all()
    serializer_class = TrainDocPostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
