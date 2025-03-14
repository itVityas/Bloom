import os
from tempfile import NamedTemporaryFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.declaration.permissions import DeclarationPermission
from apps.declaration.serializers.upload_declaration import ZipFileUploadSerializer
from apps.declaration.utils.dbf.process_all_dbf_files import process_all_dbf_files


@extend_schema(tags=['ZipUpload'])
@extend_schema_view(
    post=extend_schema(
        summary='Delete declaration',
        description='Permission: admin, declaration_writer',
    ),
)
class ZipFileUploadAPIView(APIView):
    """
    API endpoint for uploading a zip file containing DBF files.

    This endpoint accepts a zip archive containing the following files:
    DECL.DBF, G18.DBF, G40.DBF, G44.DBF, G47.DBF, G48.DBF, G313, GB.DBF, TOVAR.DBF.
    The general processing function is called to process each file accordingly.
    The uploaded zip file and all temporary extracted files are deleted after processing.
    """
    permission_classes = (IsAuthenticated, DeclarationPermission)
    serializer_class = ZipFileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_zip = serializer.validated_data['file']

        tmp_zip_path = None
        try:
            # Save uploaded zip file to a temporary file
            with NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                for chunk in uploaded_zip.chunks():
                    tmp_zip.write(chunk)
                tmp_zip_path = tmp_zip.name

            # Call the general processing function
            process_all_dbf_files(tmp_zip_path)

        except Exception as e:
            return Response({'error': f'Error processing zip file: {str(e)}'}, status=500)
        finally:
            if tmp_zip_path and os.path.exists(tmp_zip_path):
                os.remove(tmp_zip_path)

        return Response({'status': 'Zip file processed successfully.'}, status=201)
