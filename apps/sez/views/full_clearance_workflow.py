from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sez.clearance_workflow.full_clearance_workflow import (
    execute_full_clearance_workflow,
    undo_full_clearance_workflow,
    AlreadyCalculatedError, ModelClearanceEmptyError
)
from apps.sez.clearance_workflow.shtrih_service import NotEnoughProductsError
from apps.sez.clearance_workflow.vznab_stock_service import PanelError
from apps.sez.permissions import ClearanceInvoiceItemsPermission
from apps.sez.serializers.full_clearance_workflow import (
    FullClearanceWorkflowInputSerializer,
    FullClearanceWorkflowResultSerializer,
)


@extend_schema(tags=['Clearance Workflow'])
@extend_schema_view(
    post=extend_schema(
        summary='Запустить полный процесс списания и создать записи ClearedItem',
        description='Права: admin, cleared_item_writer',
        request=FullClearanceWorkflowInputSerializer,
        responses={
            200: OpenApiResponse(description='Успешный расчет'),
            400: OpenApiResponse(description='Накладная уже рассчитана'),
            404: OpenApiResponse(description='Накладная не найдена'),
            409: OpenApiResponse(description='Недостаточно товаров для списания'),
            422: OpenApiResponse(description='Проверка панели не пройдена'),
            424: OpenApiResponse(description='Нет совпадений в декларации для данной модели'),
            500: OpenApiResponse(description='Внутренняя ошибка сервера'),
        },
    ),
    delete=extend_schema(
        summary='Откатить полный процесс списания и удалить записи ClearedItem',
        description='Права: admin, cleared_item_writer',
        request=FullClearanceWorkflowInputSerializer,
        responses={
            204: OpenApiResponse(description='Успешно отменено'),
            404: OpenApiResponse(description='Накладная не найдена'),
            500: OpenApiResponse(description='Сбой при попытке отката'),
        },
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

        # 2) Execute and catch errors
        try:
            execute_full_clearance_workflow(invoice_id)
        except ObjectDoesNotExist as e:
            return Response(
                {"detail": f"Накладная с ID={invoice_id} не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )
        except AlreadyCalculatedError as e:
            return Response(
                {"detail": f"Расчёт для накладной уже выполнен: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotEnoughProductsError as e:
            return Response(
                {"detail": f"Недостаточно товаров для списания: {e}"},
                status=status.HTTP_409_CONFLICT
            )
        except PanelError as e:
            return Response(
                {"detail": f"Проверка панели не пройдена: {e}"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except ModelClearanceEmptyError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_424_FAILED_DEPENDENCY
            )
        except Exception:
            return Response(
                {"detail": "Произошла внутренняя ошибка сервера."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_200_OK)

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
                {"detail": f"Накладная с ID={invoice_id} не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {"detail": "Не удалось откатить процесс списания."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3) Return No Content
        return Response(status=status.HTTP_204_NO_CONTENT)
