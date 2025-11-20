import os
import logging
import dbf

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems, InnerTTNItems
from apps.shtrih.models import Models
from apps.omega.models import OBJ_ATTR_VALUES_1000004


logger = logging.getLogger(__name__)


TOVAR_RASHOD_FIELDS = [
    ('G031', 'N', 3),        # 0 пусто
    ('G311', 'C', 9),        # Пусто
    ('G312', 'C', 250),      # Коммерческое наименование товара
    ('G313N', 'N', 9),       # 0 Пусто
    ('G314', 'C', 8),        # Пусто
    ('G315A', 'N', 13),      # Количество товаров по ТТН
    ('G315B', 'N', 12),      # Пусто
    ('G315B1', 'N', 12),     # Пусто
    ('G316N', 'N', 2),       # ПУсто
    ('G317A', 'C', 11),      # ШТ еденицы измерения по ТТН
    ('G317B', 'C', 11),      # Пусто
    ('G317B1', 'C', 11),     # ПУто
    ('G318', 'C', 14),       # ПУсто
    ('G319', 'C', 1),        # Пусто
    ('G32', 'N', 3),         # 1 Порядковый Номер товара
    ('G33', 'C', 10),        # Пусто ТН ВЭД
    ('G34', 'C', 3),         # Пусто Код страны происхождения
    ('G35', 'N', 11),        # Пусто
    ('G361', 'C', 1),        # Пусто
    ('G362', 'C', 1),        # Пусто
    ('G363', 'C', 1),        # Пусто
    ('G364', 'C', 1),        # Пусто
    ('G371', 'C', 2),        # Пусто
    ('G372', 'C', 2),        # Пусто
    ('G38', 'N', 13),        # ВЕС нетто
    ('G38A', 'N', 13),       # 0
    ('G39', 'C', 5),         # Пусто
    ('G40N', 'N', 3),        # 0
    ('G41', 'N', 14),        # 0
    ('G41A', 'C', 3),        # Пусто
    ('G41B', 'C', 11),       # Пусто
    ('G42', 'N', 17),        # 0
    ('G43', 'C', 1),         # Пусто
    ('G44N', 'N', 3),        # 0
    ('G45', 'N', 18),        # Таможенная стоимость
    ('G46', 'N', 15),        # 0
    ('G47N', 'N', 2),        # 0
    ('DOP_NOMER', 'C', 19),  # Номер накладной R35761
    ('NOMER_GTD', 'C', 20),  # Номер ГТД, clearance_invoice.id
    ('ST_TNVED_P', 'N', 2),  # 0
    ('ST_TNVED_A', 'N', 2),  # 0
    ('ST_TNVED_N', 'N', 2),  # 0
    ('OF_DOC', 'C', 25),     # Пусто
    ('G33_P', 'C', 9),       # Пусто
    ('KONST_KOD', 'C', 20),  # Подкод товара
]


def generate_rashod_tovar_decl_dbf(
    clearance_invoice_id: int,
    output_path: str,
    encoding: str = 'cp866'
) -> None:
    """
    Generate a RASHOD_tovar-format DBF file for a given ClearanceInvoice.

    Always produces exactly one record containing invoice-level data:
      - constants for recipient (G141–G143)
      - invoice.id in G549 and NOMER_GTD      - constant '1' in G013

      - invoice.date_calc date in G542
      - user-entered TTN in DOP_NOMER
      - hardcoded country in G082
      - constant '1' in G013
      - empty values for all other fields

    Args:
        clearance_invoice_id (int): PK of the ClearanceInvoice.
        output_path (str): Full file path where the .dbf should be written.
        encoding (str, optional): Code page for the DBF. Defaults to 'cp866'.

    Raises:
        ValueError: If no ClearanceInvoice with the given ID exists.
        ValueError: If invoice.date_calc is not set.
        ValueError: If an unsupported field type is found in RASHOD_DECL_FIELDS.
        OSError: If file deletion or writing fails.
    """
    logger.info(f"Starting RASHOD_TOVAR_DECL DBF generation for invoice id={clearance_invoice_id}")

    try:
        invoice = ClearanceInvoice.objects.get(pk=clearance_invoice_id)
    except ClearanceInvoice.DoesNotExist:
        logger.error(f"ClearanceInvoice id={clearance_invoice_id} not found")
        raise ValueError(f"ClearanceInvoice with id={clearance_invoice_id} not found")

    if invoice.date_calc is None:
        logger.error("ClearanceInvoice.date_calc must be set to generate RASHOD_DECL")
        raise ValueError("ClearanceInvoice.date_calc must be set")

    # Build DBF spec
    specs = []
    for name, ftype, length in TOVAR_RASHOD_FIELDS:
        if ftype == 'C':
            specs.append(f"{name} C({length})")
        elif ftype == 'N':
            if name == 'G315A':
                specs.append(f"{name} N({length+4}, 4)")
            elif name == 'G45' or name == 'G41' or name == 'G42' or name == 'G46':
                specs.append(f"{name} N({length+2}, 2)")
            else:
                specs.append(f"{name} N({length},0)")
        elif ftype == 'L':
            specs.append(f"{name} L")
        elif ftype == 'D':
            specs.append(f"{name} D")
        else:
            logger.error(f"Unsupported field type {ftype!r} in RASHOD_DECL_FIELDS")
            raise ValueError(f"Unsupported field type {ftype!r} in RASHOD_DECL_FIELDS")
    spec_line = "; ".join(specs)
    logger.debug(f"DBF spec line built: {spec_line}")

    # Remove existing file if present
    if os.path.exists(output_path):
        os.remove(output_path)
        logger.info(f"Removed existing file at {output_path}")

    # 4. Open DBF table
    try:
        table = dbf.Table(output_path, spec_line, codepage=encoding)
        table.open(dbf.READ_WRITE)
        logger.info(f"Opened DBF table at {output_path}")
    except Exception as e:
        logger.exception(f"Failed to open DBF table at {output_path}: {e}")
        raise ValueError("Open DBF: " + str(e))

    # Build the single row
    clearance_items = ClearanceInvoiceItems.objects.filter(clearance_invoice=invoice)
    line = 1
    for clearance_item in clearance_items:
        itter_ttn_items = None
        if clearance_item.model_name_id:
            itter_ttn_items = InnerTTNItems.objects.filter(
                model_name=clearance_item.model_name_id,
                inner_ttn__uuid=invoice.ttn
            ).first()
        row = {}
        for name, ftype, *_ in TOVAR_RASHOD_FIELDS:
            if name == 'G312':
                if clearance_item.declared_item_id is not None:
                    value = clearance_item.declared_item_id.name
                else:
                    value = clearance_item.model_name_id.short_name
            elif name == 'G315A':
                value = clearance_item.quantity
            elif name == 'G317A':
                if itter_ttn_items is not None:
                    value = itter_ttn_items.measure
                    continue
                if clearance_item.declared_item_id is not None:
                    value = clearance_item.declared_item_id.measurement
                    continue
                value = ''
            elif name == 'G32':
                value = line
                line += 1
            elif name == 'G33':
                value = ''
                model = Models.objects.filter(name=clearance_item.model_name_id).first()
                if model is not None:
                    tn_ved = OBJ_ATTR_VALUES_1000004.objects.using('oracle_db').filter(A_2707=model.code).first()
                    if tn_ved:
                        value = tn_ved.A_2948
            elif name == 'G38':
                value = 1
            elif name == 'G45':
                value = 1
            elif name == 'DOP_NOMER':
                value = invoice.ttn or ''
            elif name == 'NOMER_GTD':
                inv_str = str(invoice.id)
                value = inv_str[-6:].rjust(4, '0')
            elif name == 'KONST_KOD':
                value = ''
                model = Models.objects.filter(name=clearance_item.model_name_id).first()
                if model is not None:
                    code = str(model.code)
                    # value = '0' + code[1:] + '0'
                    value = code
            else:
                # empty for fields
                if ftype == 'C':
                    value = ''
                else:
                    value = 0
            row[name] = value
        table.append(row)

    table.close()
