import os
from tempfile import NamedTemporaryFile

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    get_object_or_404, GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.declaration.filters import DeclarationFilter
from apps.arrival.models import Container
from apps.declaration.permissions import DeclarationPermission
from apps.declaration.models import Declaration

from apps.declaration.serializers.declaration import (
    DeclarationSerializer,
    DeclarationFileUploadSerializer,
    DeclarationAndItemSerializer,
    DeclarationAndItemFileUploadSerializer,
    DeclarationBindSerializer, DeclarationBulkDeleteSerializer
)
from apps.declaration.utils.dbf.decl import process_decl_dbf_file
from apps.declaration.utils.dbf.tovar import process_tovar_dbf_file

from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='List all declarations',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    post=extend_schema(
        summary='Upload file to create declarations',
        description='Permission: admin, declaration_writer',
        request=DeclarationFileUploadSerializer,
    ),
)
class DeclarationListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationSerializer
    queryset = Declaration.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeclarationFilter
    pagination_class = StandartResultPaginator

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.request.method == 'POST':
            return DeclarationFileUploadSerializer
        return DeclarationSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles file upload and processes the DBF file to create Declaration instances.
        """
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response(
                {'error': 'File not found. Please pass file with key "file".'},
                status=400
            )

        tmp_file_path = None
        try:
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            process_decl_dbf_file(tmp_file_path)

        except Exception as e:
            return Response(
                {'error': f'File processing error: {str(e)}'},
                status=500
            )

        finally:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

        return Response(
            {'status': 'File processed and declarations created.'},
            status=201
        )


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve declaration by id',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    put=extend_schema(
        summary='Update declaration',
        description='Permission: admin, declaration_writer',
    ),
    patch=extend_schema(
        summary='Partial update of declaration',
        description='Permission: admin, declaration_writer',
    ),
    delete=extend_schema(
        summary='Delete declaration',
        description='Permission: admin, declaration_writer',
    ),
)
class DeclarationDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationSerializer
    queryset = Declaration.objects.all()


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='List all declarations with items',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
)
class DeclarationAndItemView(ListAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationAndItemSerializer
    queryset = Declaration.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('container',)
    pagination_class = None


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve declaration by id with items',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
)
class DeclarationAndItemDetailedView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationAndItemSerializer
    queryset = Declaration.objects.all()


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    post=extend_schema(
        summary='Upload declarations and items files',
        description='Permission: admin, declaration_writer',
    ),
)
class DeclarationAndItemCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationAndItemFileUploadSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles file uploads for declarations and items, processes both DBF files,
        and associates the declarations with the specified container.
        """
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

        decl_tmp_file_path = None
        tovar_tmp_file_path = None

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
            return Response({'error': f'File processing error: {str(e)}'},
                            status=500)

        finally:
            if decl_tmp_file_path and os.path.exists(decl_tmp_file_path):
                os.remove(decl_tmp_file_path)
            if tovar_tmp_file_path and os.path.exists(tovar_tmp_file_path):
                os.remove(tovar_tmp_file_path)

        declarations = Declaration.objects.filter(container=container)
        declaration_serializer = DeclarationSerializer(declarations, many=True)
        return Response(declaration_serializer.data, status=201)


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    post=extend_schema(
        summary='Binds or unbinds given declarations to the specified container.',
        description='Permission: admin, declaration_writer',
    ),
)
class BindDeclarationsToContainerAPIView(APIView):
    """
    Binds given declarations to the specified container.

    If 'container_id' is null, the declarations are unbound (container set to None).
    """
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclarationBindSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        container_id = serializer.validated_data.get('container_id')
        declaration_ids = serializer.validated_data['declaration_ids']

        if container_id is not None:
            container = get_object_or_404(Container, pk=container_id)
        else:
            container = None

        updated_count = Declaration.objects.filter(id__in=declaration_ids).update(container=container)

        return Response({
            'status': f'{updated_count} declarations updated.',
            'container_id': container_id,
            'declaration_ids': declaration_ids
        })


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    delete=extend_schema(
        summary='Delete all declaration.',
        description='Permission: admin, declaration_writer',
    ),
)
class DeclarationBulkDeleteAPIView(GenericAPIView):
    """
    DELETE: Remove all Declaration records from the database.
    """
    permission_classes = (IsAuthenticated, DeclarationPermission)  # или свой Permission-класс
    serializer_class = DeclarationBulkDeleteSerializer
    queryset = Declaration.objects.all()

    def delete(self, request, *args, **kwargs):
        count, _ = Declaration.objects.all().delete()
        return Response(
            {"deleted_declarations": count},
            status=status.HTTP_200_OK
        )