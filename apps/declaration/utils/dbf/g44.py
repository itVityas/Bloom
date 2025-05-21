from apps.declaration.utils.dbf.util import clean_str, read_dbf_records
from apps.declaration.models import G44, Declaration


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
    Converts a DBF record into a dictionary mapping suitable for creating a G44.

    :param record: A record from the DBF file.
    :return: Dictionary with keys corresponding to G44 fields.
    """
    data = {
        'declaration': get_declaration(record),
        'g32': record.G32,
        'g44kd': clean_str(record.G44KD),
        'g44nd': clean_str(record.G44ND),
        'g44dd': record.G44DD,
        'g44i': record.G44I,
    }
    return data


def list_of_dict_dbf_records(records):
    """
    Creates a list of dictionaries for subsequent database insertion.

    :param records: Iterable of DBF records.
    :return: List of dictionaries.
    """
    return [dbf_to_dict(record) for record in records]


def save_g44_records_to_db(records_data):
    """
    Accepts a list of dictionaries with G44 record data,
    creates G44 instances, and saves them via bulk_create.

    :param records_data: List of dictionaries with G44 record data.
    """
    # Фильтруем записи, где удалось определить декларацию
    records = [G44(**data) for data in records_data if data['declaration']]

    if records:
        G44.objects.bulk_create(records)
        print(f"Saved {len(records)} G44 records to db.")
    else:
        print("No data to save.")


def process_g44_dbf_file(file_path):
    """
    Main function for processing the G44.DBF file.

    Reads the DBF file, converts its records to dictionaries, and saves the records
    to the database.

    :param file_path: Path to the G44.DBF file.
    """
    try:
        records = read_dbf_records(file_path)
        list_records = list_of_dict_dbf_records(records)
        save_g44_records_to_db(list_records)
    except Exception as e:
        print(f"Ошибка обработки файла G44.DBF: {e}")