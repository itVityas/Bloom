from apps.declaration.utils.dbf.util import clean_str, read_dbf_records
from apps.declaration.models import DeclaredItem, Declaration


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
    Converts a DBF record into a dictionary suitable for creating a DeclaredItem.

    :param record: A record from the DBF file.
    :return: Dictionary mapping for DeclaredItem fields.
    """
    g31stz = clean_str(record.G31STZ)
    try:
        g31stz = float(g31stz)
    finally:
        g31stz = 0.0
    g311stz = clean_str(record.G31STZ)
    try:
        g311stz = float(g311stz)
    finally:
        g311stz = 0.0
    data = {
        'declaration': get_declaration(record),
        'name': clean_str(record.G312),
        # G314 is omitted
        'ordinal_number': record.G32,
        'country_code': clean_str(record.G34),
        'alpha_country_code': clean_str(record.G34A),
        'gross_weight': record.G38,
        'quantity': record.G41,
        'unit_code': clean_str(record.G41A),
        'unit_name': clean_str(record.G41B),
        'cost': record.G42,
        'statistical_cost': record.G46,
        'payment_details_count': record.G47N,
        'document_details_count': record.G44N,
        'code': clean_str(record.G33),
        'country_name': clean_str(record.G16),
        'g37': clean_str(record.G37),
        'net_weight': record.G38A,
        'previous_customs_regime_code': clean_str(record.G372),
        'g373': clean_str(record.G373),
        'customs_cost': record.G45,
        'items_quantity': g31stz,
        'measurement_code': clean_str(record.G311STZ),
        'measurement': clean_str(record.G312STZ),
        'valuation_method': clean_str(record.G43),
        'available_quantity': g311stz,
    }
    return data


def list_of_dict_dbf_records(records):
    """
    Creates a list of dictionaries for subsequent database insertion.

    :param records: Iterable of DBF records.
    :return: List of dictionaries.
    """
    return [dbf_to_dict(record) for record in records]


def save_items_to_db(items_data):
    """
    Accepts a list of dictionaries with item data,
    creates DeclaredItem instances, and saves them via bulk_create.

    :param items_data: List of dictionaries with item data.
    """
    items = [DeclaredItem(**data) for data in items_data]

    if items:
        DeclaredItem.objects.bulk_create(items)
        print(f"Saved {len(items)} items to db.")
    else:
        print("No data to save")


def process_tovar_dbf_file(file_path):
    """
    Main function for processing the DBF file.

    :param file_path: Path to the DBF file.
    """
    try:
        records = read_dbf_records(file_path)
        list_items = list_of_dict_dbf_records(records)
        save_items_to_db(list_items)
    except Exception as e:
        print(f"Ошибка обработки файла tovar: {e}")
        raise e
