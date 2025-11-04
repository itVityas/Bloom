from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from Bloom.paginator import StandartResultPaginator
from apps.sez.models import ClearedItem
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.serializers.cleared_item_by_clearance import ClearedItemListSerializer


@extend_schema(tags=['Clearance Workflow'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить ClearedItem по ClearanceInvoice',
        description='Права: admin, cleared_item_writer, cleared_item_reader',
        responses=ClearedItemListSerializer,
    )
)
class ClearedItemListAPIView(ListAPIView):
    """
    List all ClearedItem entries for a given ClearanceInvoice.
    """
    serializer_class = ClearedItemListSerializer
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission)
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend,]

    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        return (
            ClearedItem.objects
            .filter(clearance_invoice_items__clearance_invoice_id=invoice_id)
            .select_related('declared_item_id__declaration')
            .order_by('declared_item_id__declaration__declaration_number', 'declared_item_id__ordinal_number')
        )
