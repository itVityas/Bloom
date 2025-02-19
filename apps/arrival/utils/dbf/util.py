import dbf
import re


def read_dbf_records(file_path):
    """
    Opens a DBF file and returns a list of records.

    :param file_path: Path to the DBF file.
    :return: List of records from the DBF file.
    """
    with dbf.Table(file_path) as table:
        records = list(table)
    return records


def clean_str(value):
    """
    Removes leading and trailing whitespace from the value and converts it to a string.

    :param value: The input value to be cleaned.
    :return: A string with no leading or trailing whitespace, or an empty string if value is None.
    """
    if value is None:
        return ""
    cleaned_value = re.sub(r'^\s+|\s+$', '', str(value))
    return cleaned_value
