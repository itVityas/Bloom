from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from apps.sez.clearance_workflow.vznab_stock_service import PanelError
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.clearance_workflow.full_clearance_workflow import (
    execute_full_clearance_workflow,
    undo_full_clearance_workflow,
    AlreadyCalculatedError
)
from apps.sez.clearance_workflow.shtrih_service import NotEnoughProductsError
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
        request=FullClearanceWorkflowInputSerializer,
        responses=FullClearanceWorkflowResultSerializer(many=True),
    ),
    delete=extend_schema(
        summary='Undo full clearance workflow and remove ClearedItem records',
        description='Permission: admin, cleared_item_writer',
        request=FullClearanceWorkflowInputSerializer,
        responses={204: None},
    )
)
class FullClearanceWorkflowAPIView(APIView):
    """
    API endpoint to execute or undo the full clearance workflow for a given invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoiceItemsPermission,)

    def post(self, request, *args, **kwargs):
        """
        Start the full clearance workflow:
        - timestamp the invoice
        - allocate components
        - clear declared items
        - mark products as cleared

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
        serializer = FullClearanceWorkflowInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice_id = serializer.validated_data['invoice_id']
        is_tv = serializer.validated_data['is_tv']

        # 2) Execute and catch errors
        try:
            results = execute_full_clearance_workflow(invoice_id, is_tv)
        except ObjectDoesNotExist as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except AlreadyCalculatedError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotEnoughProductsError as e:
            return Response(
                {"detail": f"Not enough products available: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PanelError as e:
            return Response(
                {"detail": f"Panel check failed: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # unexpected error
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3) Serialize and return
        out_ser = FullClearanceWorkflowResultSerializer(results, many=True)
        return Response(out_ser.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Undo the full clearance workflow:
        - restore declared_item quantities
        - delete ClearedItem records
        - reset products cleared flag
        - clear invoice timestamp

        Returns 204 No Content on success.
        """
        # 1) Validate input
        serializer = FullClearanceWorkflowInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice_id = serializer.validated_data['invoice_id']

        # 2) Perform undo and catch errors
        try:
            undo_full_clearance_workflow(invoice_id)
        except ObjectDoesNotExist:
            return Response(
                {"detail": f"ClearanceInvoice #{invoice_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {"detail": "Failed to undo clearance workflow."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3) Return No Content
        return Response(status=status.HTTP_204_NO_CONTENT)
