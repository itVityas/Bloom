from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from Bloom.paginator import StandartResultPaginator
from apps.sez.models import ClearanceResult
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.serializers.clearance_result import ClearanceResultSerializer


@extend_schema(tags=['Clearance Workflow'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve ClearanceResult invoice by ID',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    )
)
class ClearanceResultListAPIView(ListAPIView):
    """
    List all ClearedItem entries for a given ClearanceResult.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission,)
    serializer_class = ClearanceResultSerializer
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend,]

    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        return ClearanceResult.objects.filter(
            invoice_item__clearance_invoice_id=invoice_id
        ).order_by('invoice_item')

