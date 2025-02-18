import os
from tempfile import NamedTemporaryFile

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, CreateAPIView, get_object_or_404)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.arrival.permissions import ArrivalPermission
from apps.arrival.models import Declaration, Container
from apps.arrival.serializers.declaration import (
    DeclarationSerializer, DeclarationFileUploadSerializer, DeclarationAndItemSerializer,
    DeclarationAndItemFileUploadSerializer)
from apps.arrival.utils.dbf.decl import process_decl_dbf_file
from apps.arrival.utils.dbf.tovar import process_tovar_dbf_file


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

            process_decl_dbf_file(tmp_file_path)

        except Exception as e:
            return Response({'error': f'Ошибка обработки файла: {str(e)}'},
                            status=500)

        finally:
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


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Список всех деклараций с товарами',
        description='isArrivalReader, isArrivalWriter',
    ),
)
class DeclarationAndItemView(ListAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclarationAndItemSerializer
    queryset = Declaration.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filerset_fields = ('order',)
    pagination_class = None


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить декларацию по id с товарами',
        description='isArrivalReader, isArrivalWriter',
    ),
)
class DeclarationAndItemDetailedView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclarationAndItemSerializer
    queryset = Declaration.objects.all()




@extend_schema(tags=['Declarations'])
@extend_schema_view(
    post=extend_schema(
        summary='Загрузить файл деклараций и товаров',
        description='isArrivalWriter',
    ),
)
class DeclarationAndItemCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, ArrivalPermission)
    serializer_class = DeclarationAndItemFileUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container_id = serializer.validated_data.get('container_id')
        container = get_object_or_404(Container, pk=container_id)

        decl_dbf = request.FILES.get('decl_file')
        tovar_dbf = request.FILES.get('tovar_file')

        if not decl_dbf or not tovar_dbf:
            return Response(
                {'error': 'File not found. Please pass files with keys "decl_file" and "tovar_file".'},
                status=400
            )

        try:
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                for chunk in decl_dbf.chunks():
                    tmp_file.write(chunk)
                decl_tmp_file_path = tmp_file.name

            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                for chunk in tovar_dbf.chunks():
                    tmp_file.write(chunk)
                tovar_tmp_file_path = tmp_file.name

            process_decl_dbf_file(decl_tmp_file_path, container=container)
            process_tovar_dbf_file(tovar_tmp_file_path)

        except Exception as e:
            return Response({'error': f'Ошибка обработки файла: {str(e)}'},
                            status=500)

        finally:
            if os.path.exists(decl_tmp_file_path):
                os.remove(decl_tmp_file_path)
            if os.path.exists(tovar_tmp_file_path):
                os.remove(tovar_tmp_file_path)

        declarations = Declaration.objects.filter(container=container)
        declaration_serializer = DeclarationSerializer(declarations, many=True)
        return Response(declaration_serializer.data, status=201)