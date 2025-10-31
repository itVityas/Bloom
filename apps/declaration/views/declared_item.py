import os
from tempfile import NamedTemporaryFile

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.declaration.permissions import DeclarationPermission
from apps.declaration.models import DeclaredItem
from apps.declaration.serializers.declared_item import (
    DeclaredItemSerializer, DeclaredItemFileUploadSerializer
)
from apps.declaration.utils.dbf.tovar import process_tovar_dbf_file
from apps.declaration.filters import DeclarationItemFilter


@extend_schema(tags=['DeclaredItem'])
@extend_schema_view(
    get=extend_schema(
        summary='List all items',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    post=extend_schema(
        summary='Upload file to create items',
        description='Permission: admin, arrival_reader, declaration_writer',
        request=DeclaredItemFileUploadSerializer,
    ),
)
class DeclaredItemListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclaredItemSerializer
    queryset = DeclaredItem.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeclarationItemFilter
    pagination_class = None

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
        """
        if self.request.method == 'POST':
            return DeclaredItemFileUploadSerializer
        return DeclaredItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles file upload and processes the DBF file to create DeclaredItem instances.
        """
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response(
                {'error': 'File not found. Please pass file with key "file".'},
                status=400
            )

        tmp_file_path = None
        try:
            # Write uploaded file to a temporary file
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            process_tovar_dbf_file(tmp_file_path)

        except Exception as e:
            return Response(
                {'error': f'File processing error: {str(e)}'},
                status=500
            )

        finally:
            # Delete the temporary file if it exists
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

        return Response(
            {'status': 'File processed and items created.'},
            status=201
        )


@extend_schema(tags=['DeclaredItem'])
@extend_schema_view(
    get=extend_schema(
        summary='Get item by id',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    put=extend_schema(
        summary='Update item',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    patch=extend_schema(
        summary='Partial update of item',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
    delete=extend_schema(
        summary='Delete item',
        description='Permission: admin, arrival_reader, declaration_writer',
    ),
)
class DeclaredItemDetailedView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = DeclaredItemSerializer
    queryset = DeclaredItem.objects.all()
