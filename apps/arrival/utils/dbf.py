import dbf
import re
from datetime import datetime
from django.utils import timezone
from apps.arrival.models import Declaration



def read_dbf_records(file_path):
    """
    Открывает DBF-файл и возвращает список записей.
    """
    table = dbf.Table(file_path)
    table.open()
    records = [record for record in table]
    table.close()
    return records


def clean_str(value):
    if value is None:
        return ""
    cleaned_value = re.sub(r'^\s+|\s+$', '', str(value))
    return cleaned_value


def make_date_aware(dt):
    """
    Принимает наивный datetime, извлекает из него только дату и возвращает
    timezone-aware datetime с часовым поясом UTC.
    """
    if dt is None:
        return None
    # Извлекаем дату и создаём новый datetime в полночь с информацией о часовом поясе UTC.
    return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)



def dbf_to_dict(record):
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
        'declaration_id': record.DECL_ID,
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
    # Преобразуем каждый словарь в экземпляр модели Declaration
    declarations = [Declaration(**data) for data in declarations_data]

    if declarations:
        Declaration.objects.bulk_create(declarations)
        print(f"Save {len(declarations)} declarations to db.")
    else:
        print("No data to save")

def process_dbf_file(file_path):
    try:
        records = read_dbf_records(file_path)
        list_declarations = list_of_dict_dbf_records(records)
        save_declaration_to_db(list_declarations)
    except Exception as e:
        print(f"Error: {e}")

# from apps.arrival.utils.dbf import process_dbf_file
# file_path = "/home/foile/PycharmProjects/dbf_test/1245(8275)/DECL.DBF"
# process_dbf_file(file_path)