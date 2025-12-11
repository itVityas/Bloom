import logging

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from apps.sez.models import ClearanceInvoiceItems
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.serializers.clearance_invoice_items import ClearanceInvoiceItemsSerializer
from apps.shtrih.models import ModelNames
from rest_framework.response import Response

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

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f'Deleting clearance invoice item: {instance.id}')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['ClearanceInvoiceItems'])
@extend_schema_view(
    post=extend_schema(
        summary='Create empty clearance_invoice_item. Always model_name_id=589, quantity=1',
        description='Permission: admin, clearance_invoice_items_writer',
    ),
)
class ClearanceInvoiceItemsEmptyCreateAPIView(CreateAPIView):
    """
    Create multiple clearance invoice items.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission)
    serializer_class = ClearanceInvoiceItemsSerializer

    def create(self, request, *args, **kwargs):
        clearance_invoice_item = ClearanceInvoiceItems(
            clearance_invoice_id=request.data.get('clearance_invoice'),
            model_name_id=ModelNames.objects.get(id=589),
            quantity=1,
        )
        clearance_invoice_item.save()
        serializer = self.get_serializer(clearance_invoice_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
