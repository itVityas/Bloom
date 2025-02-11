import os
from tempfile import NamedTemporaryFile

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.arrival.permissions import ArrivalPermission
from apps.arrival.models import DeclaredItem
from apps.arrival.serializers.declared_item import (
    DeclaredItemSerializer, DeclaredItemFileUploadSerializer)
from apps.arrival.utils.dbf.tovar import process_tovar_dbf_file


@extend_schema(tags=['DeclaredItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех товаров',
        description='isArrivalReader, isArrivalWriter',
    ),
    post=extend_schema(
        summary='Загрузить файл для создания товаров',
        description='isArrivalWriter',
        request=DeclaredItemFileUploadSerializer,
    ),
)
class DeclaredItemListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclaredItemSerializer
    queryset = DeclaredItem.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filerset_fields = ('ordinal_number', 'declaration_id')
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeclaredItemFileUploadSerializer
        return DeclaredItemSerializer

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'File not found. '
                             'Please pass file with key "file".'}, status=400)

        try:
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            process_tovar_dbf_file(tmp_file_path)

        except Exception as e:
            return Response({'error': f'Ошибка обработки файла: {str(e)}'},
                            status=500)

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

        return Response({'status': 'Файл обработан и товары созданы.'},
                        status=201)


@extend_schema(tags=['DeclaredItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить товар по id',
        description='isArrivalReader, isArrivalWriter',
    ),
    put=extend_schema(
        summary='Обновить товар',
        description='isArrivalWritter',
    ),
    patch=extend_schema(
        summary='Частичное обновление товара',
        description='isArrivalWriter'
    ),
    delete=extend_schema(
        summary='Удалить товар',
        description='isArrivalWriter',
    ),
)
class DeclaredItemDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclaredItemSerializer
    queryset = DeclaredItem.objects.all()
