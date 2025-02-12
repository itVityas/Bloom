import dbf
import re


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
    """
    Удаляет из данных все пробелы (в том числе необычные), а также переводит в строку.
    """
    if value is None:
        return ""
    cleaned_value = re.sub(r'^\s+|\s+$', '', str(value))
    return cleaned_value

