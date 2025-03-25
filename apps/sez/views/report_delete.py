from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.sez.models import ClearanceInvoice
from apps.sez.serializers.clearance_invoice import ClearanceInvoiceSerializer
from apps.sez.permissions import ClearanceInvoicePermission


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Change cleared = false',
        description='Permission: admin, stz_reader, clearance_invoice_items_writer',
    )
)
class ReportDeleteView(UpdateAPIView):
    queryset = ClearanceInvoice.objects.all()
    serializer_class = ClearanceInvoiceSerializer
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cleared = False
        instance.save()
        serializer = ClearanceInvoiceSerializer(instance)
        return Response(serializer.data)
