from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.invoice.models import InvoiceItem
from apps.invoice.serializers.invoice_item import InvoiceItemSerializer
from apps.invoice.permissions import InvoicePermission


@extend_schema(tags=['InvoiceItem'])
@extend_schema_view(
    get=extend_schema(
        summary='List all invoice items',
        description='',
    ),
    post=extend_schema(
        summary='Create a new invoice item',
        description='',
    )
)
class InvoiceItemListCreateView(ListCreateAPIView):
    """
    API view for listing and creating InvoiceItem instances.
    """
    permission_classes = (IsAuthenticated, InvoicePermission)
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()


@extend_schema(tags=['InvoiceItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve a single invoice item',
        description='',
    ),
    put=extend_schema(
        summary='Update a single invoice item',
        description='',
    ),
    patch=extend_schema(
        summary='Partially update a single invoice item',
        description='',
    ),
    delete=extend_schema(
        summary='Delete a single invoice item',
        description='',
    ),
)
class InvoiceItemDetailedView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single InvoiceItem instance.
    """
    permission_classes = (IsAuthenticated, InvoicePermission)
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
