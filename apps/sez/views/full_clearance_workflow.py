from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.clearance_workflow.full_clearance_workflow import execute_full_clearance_workflow
from apps.sez.serializers.full_clearance_workflow import (
    FullClearanceWorkflowInputSerializer,
    FullClearanceWorkflowResultSerializer,
)
from apps.sez.models import ClearanceInvoice


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    post=extend_schema(
        summary='Run full clearance workflow and create ClearedItem records',
        description='Permission: admin, cleared_item_writer',
    ),
)
class FullClearanceWorkflowAPIView(APIView):
    """
    API endpoint to execute the full clearance workflow for a given invoice.

    POST:
        Runs the end‑to‑end pipeline:
        1. Updates missing 1C codes.
        2. Allocates components.
        3. Clears declared items.
        4. Marks Products as cleared.
        Returns detailed results for each component cleared.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission,)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to start the full clearance workflow.

        Validates input, checks invoice existence, executes the workflow,
        and returns serialized results.

        Request body:
            {
              "invoice_id": <int>,
              "is_tv": <bool>
            }

        Response (200 OK):
            [
              {
                "name": "Component A",
                "requested": 10.0,
                "plan": [
                  {"declaration_number": "000123", "cleared": 6.0},
                  {"declaration_number": "000456", "cleared": 4.0}
                ],
                "not_cleared": 0.0
              },
              ...
            ]
        """
        # 1) Validate input
        inp_ser = FullClearanceWorkflowInputSerializer(data=request.data)
        inp_ser.is_valid(raise_exception=True)
        invoice_id = inp_ser.validated_data['invoice_id']
        is_tv = inp_ser.validated_data['is_tv']

        # 2) Ensure invoice exists
        try:
            ClearanceInvoice.objects.get(pk=invoice_id)
        except ClearanceInvoice.DoesNotExist:
            raise ObjectDoesNotExist(f"ClearanceInvoice #{invoice_id} not found")

        # 3) Run workflow
        results = execute_full_clearance_workflow(invoice_id, is_tv)

        # 4) Serialize and return output
        out_ser = FullClearanceWorkflowResultSerializer(results, many=True)
        return Response(out_ser.data)
