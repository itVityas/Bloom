import os
from tempfile import NamedTemporaryFile
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
import dbf

from apps.declaration.serializers.declaration import DeclarationFileUploadSerializer
from apps.declaration.utils.dbf.util import clean_str
from apps.declaration.models import Declaration, DeclaredItem
from apps.omega.models import Stockobj
from apps.declaration.utils.get_1c import get_1c_declaration_data


def dbf_to_dict(record):
    data = {
        'GOD': clean_str(record.GOD),
        'MES': clean_str(record.MES),
        'DEN': clean_str(record.DEN),
        'KOD_DOK': clean_str(record.KOD_DOK),
        'NOM_GTD': clean_str(record.NOM_GTD),
        'DATA_GTD': clean_str(record.DATA_GTD),
        'DATA_BUH': clean_str(record.DATA_BUH),
        'NOM_TOV': clean_str(record.NOM_TOV),
        'NOM_TOV_D': clean_str(record.NOM_TOV_D),
        'SPP': clean_str(record.SPP),
        'REESTR_N': clean_str(record.REESTR_N),
        'DOKNO': clean_str(record.DOKNO),
        'POST': clean_str(record.POST),
        'KM_GTD': clean_str(record.KM_GTD),
        'EI': clean_str(record.EI),
        'PRIXOD': clean_str(record.PRIXOD),
        'PRIXOD_DET': clean_str(record.PRIXOD_DET),
        'RASXOD': clean_str(record.RASXOD),
        'PRIZ_SOST': clean_str(record.PRIZ_SOST),
        'PRIZ_LIM': clean_str(record.PRIZ_LIM),
        'VREM_V': clean_str(record.VREM_V),
        'VREM_N': clean_str(record.VREM_N),
        'VREM_K': clean_str(record.VREM_K),
        'PRIZ_UDAL': clean_str(record.PRIZ_UDAL),
        'PRIZ_KOR': clean_str(record.PRIZ_KOR),
        'DATA_P': clean_str(record.DATA_P),
        'TIME_P': clean_str(record.TIME_P),
        'KOD_MOD': clean_str(record.KOD_MOD),
        '_NullFlags': clean_str(record._NullFlags),
    }
    return data


@extend_schema(tags=['Utils'])
@extend_schema_view(
    post=extend_schema(
        summary='Upload declaration file gtd_dvi.dbf',
        description='Upload declaration file',
        request=DeclarationFileUploadSerializer,
        responses={200: None},
    ),
)
class GTDDVIFileUploadUpdateView(APIView):
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
            declaration_number = ''
            for decl in decl_list:
                available_items = float(decl['PRIXOD'])-float(decl['RASXOD'])
                try:
                    god = int(decl['GOD'])
                except Exception:
                    continue
                if available_items <= 0:
                    continue
                # if available_items <= 0 and god >= 2024:
                #     available_items = float(decl['PRIXOD'])
                if decl['PRIZ_UDAL'] == 'd':
                    continue
                try:
                    decl_item = DeclaredItem.objects.filter(
                        declaration__declaration_number=decl['NOM_GTD'],
                        ordinal_number=decl['NOM_TOV']
                    ).first()
                    if decl_item:
                        if decl_item.available_quantity != round(available_items, 3):
                            count += 1
                            decl_item.available_quantity = round(available_items, 3)
                            decl_item.save(update_fields=['available_quantity'])
                except Exception as e:
                    print(e)
                continue

        except Exception as e:
            return Response(
                {'detail': f'Ошибка обработки zip-файла: {str(e)}'},
                status=400
            )
        finally:
            if tmp_dbf_path and os.path.exists(tmp_dbf_path):
                os.remove(tmp_dbf_path)
        
        decl_item = DeclaredItem.objects.exclude(code='old')
        for i in decl_item:
            if i.available_quantity != i.items_quantity:
                i.available_quantity = i.items_quantity
                i.save(update_fields=['available_quantity'])
                count += 1

        return Response({'add_count': count}, status=200)
