import os
from tempfile import NamedTemporaryFile

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.arrival.models import Container
from apps.declaration.permissions import DeclarationPermission
from apps.declaration.serializers.upload_declaration import ZipFileUploadSerializer
from apps.declaration.utils.dbf.duplicate_exception import DuplicateDeclarationException
from apps.declaration.utils.dbf.process_all_dbf_files import process_all_dbf_files


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    post=extend_schema(
        summary='Upload a zip file, for create declarations',
        description='Permission: admin, declaration_writer',
    ),
)
class ZipFileUploadAPIView(APIView):
    """
    API endpoint for uploading a zip file containing DBF files.

    The endpoint accepts a zip archive containing the following files:
    DECL.DBF, G18.DBF, G40.DBF, G44.DBF, G47.DBF, G48.DBF, G313, GB.DBF, TOVAR.DBF.
    Optionally, a container_id can be provided to bind declarations (from DECL.DBF)
    to a specific container.
    The general processing function is called to process each file accordingly.
    The uploaded zip file and all temporary extracted files are deleted after processing.
    """
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = ZipFileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_zip = serializer.validated_data['file']
        container_id = serializer.validated_data.get('container_id')

        container = None
        if container_id is not None:
            from apps.arrival.models import Container
            container = get_object_or_404(Container, pk=container_id)

        tmp_zip_path = None
        try:
            with NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                for chunk in uploaded_zip.chunks():
                    tmp_zip.write(chunk)
                tmp_zip_path = tmp_zip.name

            process_all_dbf_files(tmp_zip_path, container=container)
        except DuplicateDeclarationException as de:
            return Response({'error': str(de)}, status=409)
        except Exception as e:
            return Response({'error': f'Error processing zip file: {str(e)}'}, status=500)
        finally:
            if tmp_zip_path and os.path.exists(tmp_zip_path):
                os.remove(tmp_zip_path)

        return Response({'status': 'Zip file processed successfully.'}, status=201)