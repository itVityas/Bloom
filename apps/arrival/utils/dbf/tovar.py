from apps.arrival.utils.dbf.util import clean_str, read_dbf_records
from apps.arrival.models import DeclaredItem, Declaration



def get_declaration(record):
    """
    Пытается получить экземпляр модели Declaration с DECL_ID из dbf файла
    """
    if record.DECL_ID:
        decl_id = int(clean_str(record.DECL_ID))
        try:
            declaration_instance = Declaration.objects.get(declaration_id=decl_id)
        except Declaration.DoesNotExist:
            raise ValueError(f"Declaration with declaration_id {decl_id} not found.")
    else:
        declaration_instance = None
    return declaration_instance


def dbf_to_dict(record):
    """
    Принимает строку из dbf файла и записывает их в словарь.
    """

    data = {
        'declaration_id': get_declaration(record),
        'name': clean_str(record.G312),
        # G314 / пропущен
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
        'declaration': int(clean_str(record.DECL_ID)),
        'code': clean_str(record.G33),
        'country_name': clean_str(record.G16),
        'g37': clean_str(record.G37),
        'net_weight': record.G38A,
        'previous_customs_regime_code': clean_str(record.G372),
        'g373': clean_str(record.G373),
        'customs_cost': record.G45,
        'g31stz': clean_str(record.G31STZ),
        'g311stz': clean_str(record.G311STZ),
        'g312STZ': clean_str(record.G312STZ),
        # G15, G15A, G15A_0, G15A_1 / пропущены
        # G17, G17A, G17A_0, G17A_1 / пропущены
        # CODE_CORR / пропущен
        'valuation_method': clean_str(record.G43),
        # G21_A, G21_0, G21_1 / пропущены
    }
    return data


def list_of_dict_dbf_records(records):
    """
    Создает список из словарей для последующего записи в бд
    """
    items_data = []
    for record in records:
        record = dbf_to_dict(record)
        items_data.append(record)
    return items_data


def save_items_to_db(items_data):
    """
    Принимает список словарей с данными товаров,
    создает экземпляры модели DeclaredItem и сохраняет их через bulk_create.
    """
    items = [DeclaredItem(**data) for data in items_data]

    if items:
        DeclaredItem.objects.bulk_create(items)
        print(f"Save {len(items)} items to db.")
    else:
        print("No data to save")


def process_tovar_dbf_file(file_path):
    """
    Общая функция для обработки dbf файла
    """
    try:
        records = read_dbf_records(file_path)
        list_items = list_of_dict_dbf_records(records)
        save_items_to_db(list_items)
    except Exception as e:
        print(f"Error: {e}")