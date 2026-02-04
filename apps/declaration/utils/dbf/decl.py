import requests

from apps.declaration.utils.dbf.duplicate_exception import DuplicateDeclarationException
from apps.declaration.utils.dbf.util import clean_str, read_dbf_records
from apps.declaration.models import Declaration
from Bloom import settings


def dbf_to_dict(record):
    """
    Converts a DBF record into a dictionary mapping suitable for the Declaration model.

    :param record: A record from the DBF file.
    :return: A dictionary containing Declaration field values.
    """
    data = {
        'type_code': clean_str(record.G011),
        'type': clean_str(record.G012_1),
        'sender': clean_str(record.G022),
        'sender_address': clean_str(record.G023),
        'delivery_terms': clean_str(record.G20),
        'item_count': record.G05,
        'receiver': clean_str(record.G082),
        'receiver_address': clean_str(record.G083),
        'sender_country_code': clean_str(record.G15A),
        'sender_alpha_country_code': clean_str(record.G15A_0),
        'g15A_1': clean_str(record.G15A_1),
        'payment_currency_code': clean_str(record.G221),
        'total_cost': record.G222,
        'currency_rate': record.G23,
        'foreign_economic_code': clean_str(record.G241),
        'payment_type_code': clean_str(record.G242),
        'provision_date': record.G542,
        'paid_payment_details_count': record.GBN,
        'declaration_id': int(clean_str(record.DECL_ID)),
        'declaration_number': clean_str(record.NOM_REG),
        'permit_number': clean_str(record.GA),
        'country_name': clean_str(record.G16),
        'declarant_position': clean_str(record.G545),
        'declarant_FIO': clean_str(record.G546),
        'document_id': clean_str(record.DOCUMENTID),
        'sender_country_name': clean_str(record.G15),
        'outgoing_number': clean_str(record.G544),
        'dollar_rate': record.G47_KD,
        'euro_rate': record.G47_KS,
        'declaration_date': record.DATEC,
        'permit_code': clean_str(record.G013),
    }
    return data


def list_of_dict_dbf_records(records):
    """
    Creates a list of dictionaries for subsequent database insertion.

    :param records: Iterable of DBF records.
    :return: List of dictionaries.
    """
    return [dbf_to_dict(record) for record in records]


def save_declaration_to_db(declarations_data):
    """
    Accepts a list of dictionaries with Declaration data, creates Declaration instances,
    and saves them using bulk_create.

    :param declarations_data: List of dictionaries with Declaration field values.
    :raises Exception: If any declaration already exists or if no data is provided.
    """
    declarations = []
    duplicate_ids = []
    json_data = []

    for data in declarations_data:
        if Declaration.objects.filter(declaration_id=data['declaration_id']).exists():
            duplicate_ids.append(data['declaration_number'])
        else:
            declarations.append(Declaration(**data))
            buf_dict = {}
            buf_dict['code'] = data['declaration_number']
            buf_dict['name'] = data['permit_number']
            json_data.append(buf_dict)

    if duplicate_ids:
        raise DuplicateDeclarationException(duplicate_ids)
    elif declarations:
        Declaration.objects.bulk_create(declarations)

        # отправка в 1с деклараций
        gtd_url_1c = 'http://192.168.2.2/VITYAS-2/hs/bloom/data/'
        # gtd_url_1c = 'http://192.168.2.2/VITYAS-2/hs/bloom/data/'
        response = requests.post(
            gtd_url_1c,
            json={'gtd_numbers': json_data},
            auth=(settings.API_USERNAME, settings.API_PASSWORD),
            timeout=30
        )
        response.raise_for_status()

    else:
        raise Exception("Нет данных для сохранения.")


def process_decl_dbf_file(file_path, container=None, gifted=False):
    """
    Main function for processing a DBF file containing Declaration data.

    :param file_path: Path to the DBF file.
    :param container: Optional container instance to associate with each declaration.
    :param gifted: Optional flag indicating whether the declarations are gifted.
    :raises Exception: Propagates any exceptions encountered during processing.
    """
    records = read_dbf_records(file_path)
    list_declarations = list_of_dict_dbf_records(records)

    if container:
        for data in list_declarations:
            data['container'] = container
    if gifted:
        for data in list_declarations:
            data['gifted'] = gifted

    save_declaration_to_db(list_declarations)
