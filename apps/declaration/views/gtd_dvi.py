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
class GTDDVIFileUploadView(APIView):
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
                print(tmp_dbf_path)

            table = dbf.Table(tmp_dbf_path)
            table.open()
            decl_list = [dbf_to_dict(record) for record in table]
            table.close()

            count = 0
            declaration_number = ''
            for decl in decl_list:
                available_items = float(decl['PRIXOD'])-float(decl['RASXOD'])
                if available_items == 0:
                    continue
                if declaration_number != decl['NOM_GTD']:
                    try:
                        declaration = Declaration.objects.get_or_create(
                            type_code='ИМ',
                            type='ЭД',
                            sender='old',
                            sender_address='old',
                            delivery_terms='old',
                            item_count=0,
                            receiver='old',
                            receiver_address='old',
                            sender_country_code='old',
                            sender_alpha_country_code='old',
                            g15A_1='old',
                            payment_currency_code='old',
                            total_cost=0,
                            currency_rate=0,
                            foreign_economic_code='old',
                            payment_type_code='old',
                            provision_date=datetime.date.today(),
                            paid_payment_details_count=0,
                            declaration_id=decl['NOM_GTD'].split('/')[-1],
                            declaration_number=decl['NOM_GTD'],
                            permit_number='old',
                            country_name='old',
                            declarant_position='automatic',
                            declarant_FIO='automatic',
                            document_id='old',
                            sender_country_name='old',
                            outgoing_number='old',
                            dollar_rate=0,
                            euro_rate=0,
                            declaration_date=datetime.date(year=int(decl['GOD']), month=int(decl['MES']), day=int(decl['DEN'])),
                            permit_code='old',
                        )
                        declaration_number = decl['NOM_GTD']
                    except Exception as e:
                        print(e)
                        continue
                try:
                    if not declaration:
                        continue
                    # print(decl['NOM_GTD'])
                    DeclaredItem.objects.create(
                        declaration=declaration[0],
                        factory_code=None,
                        is_selected=None,
                        name='old',
                        ordinal_number=decl['NOM_TOV'],
                        country_code='old',
                        alpha_country_code='old',
                        gross_weight=0,
                        quantity=None,
                        unit_code='old',
                        unit_name='old',
                        cost=0,
                        statistical_cost=0,
                        payment_details_count=0,
                        document_details_count=0,
                        code='old',
                        country_name='old',
                        g37='',
                        net_weight=0,
                        previous_customs_regime_code='',
                        g373='old',
                        customs_cost=0,
                        items_quantity=float(decl['PRIXOD']),
                        measurement_code='old',
                        measurement=decl['EI'],
                        valuation_method='',
                        available_quantity=available_items,
                        item_code_1c=int(decl['KM_GTD'])
                    )
                except Exception as e:
                    print(e)
                    continue
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
