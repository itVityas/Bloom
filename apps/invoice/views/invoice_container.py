from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.invoice.models import InvoiceContainer
from apps.invoice.serializers.invoice_container import (
    InvoiceContainerGetSerializer,
    InvoiceContainerPostSerializer
)
from apps.invoice.permissions import InvoicePermission
from Bloom.paginator import StandartResultPaginator
from apps.invoice.filters import InvoiceContainerFilter


@extend_schema(tags=['InvoiceContainer'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new invoice container',
        description="Permission: 'admin', 'invoice_writer'",
    )
)
class InvoiceContainerCreateAPIView(CreateAPIView):
    """Create a new invoice container."""
    queryset = InvoiceContainer.objects.all()
    serializer_class = InvoiceContainerPostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=['InvoiceContainer'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a list of invoice containers',
        description="Permission: 'admin', 'arrival_reader', 'invoice_reader'"
    )
)
class InvoiceContainerListAPIView(ListAPIView):
    """Get a list of invoice containers."""
    queryset = InvoiceContainer.objects.all()
    serializer_class = InvoiceContainerGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvoiceContainerFilter
    pagination_class = StandartResultPaginator


@extend_schema(tags=['InvoiceContainer'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a single invoice container',
        description="Permission: 'admin', 'arrival_reader', 'invoice_reader'"
    ),
    put=extend_schema(
        summary='Update a single invoice container',
        description="Permission: 'admin', 'invoice_writer'",
    ),
    patch=extend_schema(
        summary='Update a single invoice container',
        description="Permission: 'admin', 'invoice_writer'",
    ),
    delete=extend_schema(
        summary='Delete a single invoice container',
        description="Permission: 'admin', 'invoice_writer'",
    )
)
class InvoiceContainerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Get, update or delete a single invoice container."""
    queryset = InvoiceContainer.objects.all()
    serializer_class = InvoiceContainerPostSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]


@extend_schema(tags=['InvoiceContainer'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a single invoice container',
        description="Permission: 'admin', 'arrival_reader', 'invoice_reader'"
    )
)
class InvoiceContainerRetrieveAPIView(RetrieveAPIView):
    """Get a single invoice container."""
    queryset = InvoiceContainer.objects.all()
    serializer_class = InvoiceContainerGetSerializer
    permission_classes = [IsAuthenticated, InvoicePermission]
