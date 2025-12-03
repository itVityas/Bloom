from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.sreport.serializers.report_storage import ReportStorageSerializer
from apps.sreport.models import ReportStorage


@extend_schema(tags=['Warehouse report'])
@extend_schema_view(
    get=extend_schema(
        description='Get products from shtrih',
        responses={200: ReportStorageSerializer},
        methods=["GET"],
    )
)
class ReportStorageView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportStorageSerializer
    queryset = ReportStorage.objects.all()

    def get(self, request):
        try:
            queryset = self.queryset.all()
            serializer = ReportStorageSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class ReportStorageView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ReportStorageSerializer

#     def get(self, request):
#         try:
#             '''
#             3: Отгрузка по накладной клиентам
#             4: Отгрузка на перевозку
#             5: Отгрузка клиентам из производства
#             6: Отгрузка на доработку в производство
#             '''
#             # Products которые есть на складе, которые не отгружены
#             shipments = [3, 4, 5, 6]
#             products_list_id = set(WarehouseProduct.objects.exclude(
#                     warehousedo__warehouse_ttn__warehouse_action__id__in=shipments
#                 ).values_list('product_id', flat=True))

#             # Количество уникальных моделей на складе
#             model_names_list_id = set(Products.objects.filter(
#                 id__in=products_list_id).values_list('model__name', flat=True))

#             result_list = []
#             for models_id in model_names_list_id:
#                 model_dict = {}
#                 model = ModelNames.objects.get(id=models_id)
#                 model_dict['model_name'] = model.short_name if model.short_name else model.name
#                 model_dict['model_name_id'] = models_id

#                 products_qs = Products.objects.filter(model__name=models_id, id__in=products_list_id)
#                 model_dict['uncleared'] = products_qs.filter(cleared__isnull=True).count()
#                 model_dict['cleared'] = products_qs.filter(cleared__isnull=False).count()
#                 model_dict['simple'] = ProductTransitions.objects.filter(
#                     new_product__in=products_qs).count()
#                 model_dict['total'] = model_dict['uncleared'] + model_dict['cleared'] + model_dict['simple']
#                 model_dict['compensation'] = products_qs.filter(protocols__invoice__recipient=4).count()
#                 result_list.append(model_dict)

#             serializer = ReportStorageSerializer(result_list, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
