from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

from apps.sez.serializers.full_clearance_workflow import (
    ClearanceDeleteInputSerializer,
    ClearanceCalculateInputSerializer
)
from apps.sez.permissions import STZPermission
from apps.sez.clearance_workflow.calculate.clear import clear_invoice_calculate
from apps.sez.clearance_workflow.calculate.calculate import begin_calculation
from apps.sez.exceptions import (
    InvoiceNotFoundException,
    InvoiceAlreadyClearedException,
    ProductsNotEnoughException,
    InternalException,
    OracleException,
    PanelException,
)


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    post=extend_schema(
        summary='Запустить полный процесс списания и создать записи ClearedItem',
        description='Права: admin, cleared_item_writer',
        request=ClearanceCalculateInputSerializer,
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
        request=ClearanceDeleteInputSerializer,
        responses={
            204: OpenApiResponse(description='Успешно очищено'),
            404: OpenApiResponse(description='Накладная не найдена'),
            500: OpenApiResponse(description='Сбой при попытке отката'),
        },
    )
)
class FullClearanceWorkflowView(APIView):
    permission_classes = [IsAuthenticated, STZPermission]

    def post(self, request):
        serializer = ClearanceCalculateInputSerializer(data=request.data)
        if serializer.is_valid():
            invoice_id = serializer.validated_data['invoice_id']
            try:
                begin_calculation(invoice_id)
                return Response({'message': 'Успешный расчет'}, status=status.HTTP_200_OK)
            except InvoiceNotFoundException:
                return Response({'error': 'Накладная не найдена'}, status=status.HTTP_404_NOT_FOUND)
            except InvoiceAlreadyClearedException:
                return Response({'error': 'Накладная уже рассчитана'}, status=status.HTTP_400_BAD_REQUEST)
            except ProductsNotEnoughException:
                return Response({'error': str(ProductsNotEnoughException)},
                                status=status.HTTP_409_CONFLICT)
            except InternalException:
                return Response({'error': str(InternalException)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except OracleException:
                return Response({'error': str(OracleException)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except PanelException:
                return Response({'error': str(PanelException)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = ClearanceDeleteInputSerializer(data=request.data)
        if serializer.is_valid():
            invoice_id = serializer.validated_data['invoice_id']
            try:
                clear_invoice_calculate(invoice_id)
                return Response({'message': 'Успешно очищено'}, status=status.HTTP_204_NO_CONTENT)
            except InvoiceNotFoundException:
                return Response({'error': 'Накладная не найдена'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
