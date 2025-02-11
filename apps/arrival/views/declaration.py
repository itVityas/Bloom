import os
from tempfile import NamedTemporaryFile

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.arrival.permissions import ArrivalPermission
from apps.arrival.models import Declaration
from apps.arrival.serializers.declaration import (
    DeclarationSerializer, DeclarationFileUploadSerializer)
from apps.arrival.utils.dbf import process_dbf_file


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех деклараций',
        description='isArrivalReader, isArrivalWriter',
    ),
    post=extend_schema(
        summary='Загрузить файл для создания декларации',
        description='isArrivalWriter',
        request=DeclarationFileUploadSerializer,
    ),
)
class DeclarationListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclarationSerializer
    queryset = Declaration.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filerset_fields = ('order', 'declaration_id')
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeclarationFileUploadSerializer
        return DeclarationSerializer

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

            process_dbf_file(tmp_file_path)

        except Exception as e:
            return Response({'error': f'Ошибка обработки файла: {str(e)}'},
                            status=500)

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

        return Response({'status': 'Файл обработан и декларации созданы.'},
                        status=201)


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить декларацию по id',
        description='isArrivalReader, isArrivalWriter',
    ),
    put=extend_schema(
        summary='Обновить декларацию',
        description='isArrivalWritter',
    ),
    patch=extend_schema(
        summary='Частичное обновление декларации',
        description='isArrivalWriter'
    ),
    delete=extend_schema(
        summary='Удалить декларацию',
        description='isArrivalWriter',
    ),
)
class DeclarationDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclarationSerializer
    queryset = Declaration.objects.all()
