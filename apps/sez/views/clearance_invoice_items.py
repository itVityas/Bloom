from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
import logging

from apps.sez.models import ClearanceInvoiceItems
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.serializers.clearance_invoice_items import ClearanceInvoiceItemsSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=['ClearanceInvoiceItems'])
@extend_schema_view(
    get=extend_schema(
        summary='List all clearance invoice items',
        description='Permission: admin, stz_reader, clearance_invoice_items_writer',
    ),
    post=extend_schema(
        summary='Create a clearance invoice item',
        description='Permission: admin, clearance_invoice_items_writer',
    ),
)
class ClearanceInvoiceItemListCreateAPIView(ListCreateAPIView):
    """
    List all clearance invoice items or create a new clearance invoice item.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission)
    serializer_class = ClearanceInvoiceItemsSerializer
    queryset = ClearanceInvoiceItems.objects.all()


@extend_schema(tags=['ClearanceInvoiceItems'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve clearance invoice item by ID',
        description='Permission: admin, stz_reader, clearance_invoice_items_writer',
    ),
    put=extend_schema(
        summary='Update clearance invoice item',
        description='Permission: admin, clearance_invoice_items_writer',
    ),
    patch=extend_schema(
        summary='Partial update clearance invoice item',
        description='Permission: admin, clearance_invoice_items_writer',
    ),
    delete=extend_schema(
        summary='Delete clearance invoice item',
        description='Permission: admin, clearance_invoice_items_writer',
    ),
)
class ClearanceInvoiceItemDetailedView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a clearance invoice item.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission)
    serializer_class = ClearanceInvoiceItemsSerializer
    queryset = ClearanceInvoiceItems.objects.all()
