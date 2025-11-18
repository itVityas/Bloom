import os
from tempfile import NamedTemporaryFile

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
import dbf

from apps.declaration.serializers.declaration import DeclarationFileUploadSerializer
from apps.declaration.utils.dbf.util import clean_str
from apps.declaration.models import Declaration


def dbf_to_dict(record):
    data = {
        'GA': clean_str(record.GA),
        'DATAO': clean_str(record.DATAO),
        'GTDGA': clean_str(record.GTDGA),
    }
    return data


@extend_schema(tags=['Utils'])
@extend_schema_view(
    post=extend_schema(
        summary='Upload declaration file gtd_ga.dbf',
        description='Upload declaration file',
        request=DeclarationFileUploadSerializer,
        responses={200: None},
    ),
)
class GTDGAFileUploadView(APIView):
    def post(self, request):
        serializer = DeclarationFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dbf_file = serializer.validated_data['file']

        tmp_dbf_path = None
        try:
            with NamedTemporaryFile(delete=False, suffix=".dbf") as tmp_dbf:
                for chunk in dbf_file.chunks():
                    tmp_dbf.write(chunk)
                tmp_dbf_path = tmp_dbf.name

            table = dbf.Table(tmp_dbf_path)
            table.open()
            decl_list = [dbf_to_dict(record) for record in table]
            table.close()

            count = 0
            for decl_line in decl_list[::-1]:
                if decl_line.get('GTDGA') and len(decl_line.get('GTDGA').split('/')) == 3:
                    decl = Declaration.objects.filter(
                        declaration_number=str(decl_line['GA']).strip()
                    ).first()
                    if decl:
                        decl.permit_number = decl_line['GTDGA']
                        decl.save()
                        count += 1

        except Exception as e:
            return Response(
                {'detail': f'Ошибка обработки zip-файла: {str(e)}'},
                status=400
            )
        finally:
            if tmp_dbf_path and os.path.exists(tmp_dbf_path):
                os.remove(tmp_dbf_path)

        return Response({'add_count': count}, status=200)
