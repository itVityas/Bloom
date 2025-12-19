from apps.declaration.utils.dbf.util import clean_str, read_dbf_records
from apps.declaration.models import G313, Declaration


def get_declaration(record):
    """
    Tries to retrieve a Declaration instance using DECL_ID from the DBF record.

    :param record: A record from the DBF file.
    :return: Declaration instance or None.
    :raises ValueError: If the Declaration is not found.
    """
    if record.DECL_ID:
        decl_id = int(clean_str(record.DECL_ID))
        try:
            declaration_instance = Declaration.objects.get(declaration_id=decl_id)
        except Declaration.DoesNotExist:
            raise ValueError(f"Декларация с declaration_id {decl_id} не найдена.")
    else:
        declaration_instance = None
    return declaration_instance


def dbf_to_dict(record):
    """
    Converts a DBF record into a dictionary suitable for creating a G313.

    :param record: A record from the DBF file.
    :return: Dictionary mapping for G313 fields.
    """
    data = {
        'declaration': get_declaration(record),
        'g32': record.G32,
        'g313i': record.G313I,
        'g31_nm': clean_str(record.G31_NM),
        'g31_tm': clean_str(record.G31_TM),
        'g31_pb': clean_str(record.G31_PB),
        'g31_pm': clean_str(record.G31_PM),
        'g31_mg': clean_str(record.G31_MG),
        'g31_sp': clean_str(record.G31_SP),
        'g31_sn': clean_str(record.G31_SN),
        'g31_vg': clean_str(record.G31_VG),
        'g31_rd': record.G31_RD,
        'g31_qg': record.G31_QG,
        'g31_nu': clean_str(record.G31_NU),
        'g31_cu': clean_str(record.G31_CU),
        'g31_gg': clean_str(record.G31_GG),
    }
    return data


def list_of_dict_dbf_records(records):
    """
    Creates a list of dictionaries for subsequent database insertion.

    :param records: Iterable of DBF records.
    :return: List of dictionaries.
    """
    return [dbf_to_dict(record) for record in records]


def save_g313_records_to_db(records_data):
    """
    Accepts a list of dictionaries with G313 record data,
    creates G313 instances, and saves them via bulk_create.

    :param records_data: List of dictionaries with G313 record data.
    """
    records = [G313(**data) for data in records_data if data['declaration']]

    if records:
        G313.objects.bulk_create(records)
        print(f"Saved {len(records)} G313 records to db.")
    else:
        print("No data to save.")


def process_g313_dbf_file(file_path):
    """
    Main function for processing the G313.DBF file.

    :param file_path: Path to the DBF file.
    """
    try:
        records = read_dbf_records(file_path)
        list_records = list_of_dict_dbf_records(records)
        save_g313_records_to_db(list_records)
    except Exception as e:
        print(f"Ошибка обработки файла G313.DBF: {e}")
        raise e
