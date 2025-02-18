from apps.arrival.utils.dbf.util import clean_str, read_dbf_records
from apps.arrival.models import Declaration


def dbf_to_dict(record):
    """
    Принимает строку из dbf файла и записывает их в словарь.
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
    Создает список из словарей для последующего записи в бд
    """
    declarations_data = []
    for record in records:
        record = dbf_to_dict(record)
        declarations_data.append(record)
    return declarations_data


def save_declaration_to_db(declarations_data):
    """
    Принимает список словарей с данными деклараций,
    создает экземпляры модели Declaration и сохраняет их через bulk_create.
    """
    declarations = []
    declarations_exist = []

    for data in declarations_data:
        if not Declaration.objects.filter(declaration_id=data['declaration_id']).exists():
            declarations.append(Declaration(**data))
        else:
            declarations_exist.append(data['declaration_id'])

    if declarations_exist:
        raise Exception(f"Declarations {declarations_exist} already exists")
    elif declarations:
        Declaration.objects.bulk_create(declarations)
        print(f"Save {len(declarations)} declarations to db.")
    else:
        raise Exception("No data to save")


def process_decl_dbf_file(file_path, container=None):
    """
    Общая функция для обработки dbf файла
    """
    try:
        records = read_dbf_records(file_path)
        list_declarations = list_of_dict_dbf_records(records)
        if container:
            for data in list_declarations:
                data['container'] = container
        save_declaration_to_db(list_declarations)
    except Exception as e:
        raise e