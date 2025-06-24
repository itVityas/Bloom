import os
import logging
import dbf
from django.db import transaction
from django.db.models import Prefetch

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems, ClearedItem
from apps.declaration.models import Declaration

logger = logging.getLogger(__name__)


# Список деклараций
PRIHOD_DECL_FIELDS = [
    ('G549',      'C',  18, 0),      # Номер декларации, Declaration.declaration_number
    ('G011',      'C',   2, 0),      # Пусто
    ('G012',      'C',   2, 0),      # Пусто
    ('G013',      'C',   2, 0),      # Везде 7
    ('G021',      'C',   9, 0),      # Пусто
    ('G022',      'C',  38, 0),      # Отправитель, Declaration.sender
    ('G023',      'C',  76, 0),      # Пусто
    ('G031',      'N',   3, 0),      # Пусто
    ('G032',      'N',   3, 0),      # Пусто
    ('G04',       'C',   4, 0),      # Пусто
    ('G041',      'N',   4, 0),      # Пусто
    ('G05',       'N',   3, 0),      # Пусто
    ('G06',       'C',   5, 0),      # Пусто
    ('G081',      'C',   9, 0),      # Пусто
    ('G082',      'C',  38, 0),      # Отправитель, Declaration.sender
    ('G083',      'C',  76, 0),      # Пусто
    ('G091',      'C',   9, 0),      # Пусто
    ('G092',      'C',  38, 0),      # Пусто
    ('G093',      'C',  76, 0),      # Пусто
    ('G10',       'C',   2, 0),      # Пусто
    ('G11',       'C',   3, 0),      # Пусто
    ('G11_1',     'C',   4, 0),      # Пусто
    ('G12',       'N',  18, 2),      # Пусто
    ('G13',       'C',   3, 0),      # Пусто
    ('G141',      'C',   9, 0),      # УНП Витязя, 300031652
    ('G142',      'C',  38, 0),      # Получатель, РУПП "Витязь"
    ('G143',      'C',  76, 0),      # Адрес, "РБ, 210605, Г.ВИТЕБСК, УЛ.П.БРОВКИ 13А"
    ('G15',       'C',  17, 0),      # Пусто
    ('G15A',      'C',   3, 0),      # Пусто
    ('G15A_1',    'C',   4, 0),      # Пусто
    ('G16',       'C',  17, 0),      # Пусто
    ('G17',       'C',  17, 0),      # Пусто
    ('G17A',      'C',   3, 0),      # Пусто
    ('G17A_1',    'C',   4, 0),      # Пусто
    ('G18N',      'C',   2, 0),      # Пусто
    ('G19',       'C',   1, 0),      # Пусто
    ('G20N',      'N',   2, 0),      # Пусто
    ('G21N',      'C',   2, 0),      # Пусто
    ('G221',      'C',   3, 0),      # Пусто
    ('G222',      'N',  17, 2),      # Пусто
    ('G23',       'N',  10, 2),      # Пусто
    ('G23A',      'C',   6, 0),      # Пусто
    ('G241',      'C',   3, 0),      # Пусто
    ('G242',      'C',   2, 0),      # Пусто
    ('G251',      'C',   2, 0),      # Пусто
    ('G261',      'C',   2, 0),      # Пусто
    ('G27',       'C',  12, 0),      # Пусто
    ('G281',      'C',   9, 0),      # Пусто
    ('G282',      'C',  70, 0),      # Пусто
    ('G283',      'C',   8, 0),      # Пусто
    ('G284',      'C',  20, 0),      # Пусто
    ('G285',      'C',   2, 0),      # Пусто
    ('G29',       'C',   8, 0),      # Пусто
    ('G29A',      'C',  18, 0),      # Пусто
    ('G30',       'C',  15, 0),      # Пусто
    ('G30A',      'C',  18, 0),      # Пусто
    ('G47_KD',    'N',  10, 2),      # Пусто
    ('G47_KS',    'N',  10, 2),      # Пусто
    ('G48N',      'N',   2, 0),      # Пусто
    ('G49',       'C',  15, 0),      # Пусто
    ('G49A',      'C',  15, 0),      # Пусто
    ('G51',       'C',  15, 0),      # Пусто
    ('G53',       'C',  30, 0),      # Пусто
    ('G541',      'C',  60, 0),      # Пусто
    ('G541_1',    'C',   9, 0),      # Пусто
    ('G542',      'D',   8, 0),      # Дата декларации, Declaration.declaration_date
    ('G543',      'C',  15, 0),      # Пусто
    ('G544',      'C',  15, 0),      # Пусто
    ('G545',      'C',  41, 0),      # Пусто
    ('G546',      'C',  20, 0),      # Пусто
    ('G547',      'C',  26, 0),      # Пусто
    ('G548',      'C',   6, 0),      # Пусто
    ('G540_1',    'C',   9, 0),      # Пусто
    ('G540_2',    'C',   8, 0),      # Пусто
    ('G540_3',    'C',   8, 0),      # Пусто
    ('GB1PS',     'C',  64, 0),      # Пусто
    ('GB2PS',     'C',  64, 0),      # Пусто
    ('GBN',       'N',   2, 0),      # Пусто
    ('GC',        'C',  40, 0),      # Пусто
    ('GC1',       'C',   8, 0),      # Пусто
    ('GC2',       'C',   8, 0),      # Пусто
    ('GCN',       'C',   2, 0),      # Пусто
    ('DNOM_REG',  'C',  18, 0),      # Нужно взять Declaration.declaration_number (имеют вид 07260/52002951) убрать '/', оставить первые 7 символов и добавить вначало 'd', по итогу получаем d0726052
    ('DSK1',      'C',  10, 0),      # Нужно взять Declaration.declaration_number (имеют вид 07260/52002951), взять первый символ после '/' и последние 5 символов. По итогу получаем 502951
    ('D2PRIM',    'C', 160, 0),      # Пусто
    ('GK_A',      'C',   1, 0),      # Пусто
    ('DOP_NOMER', 'C',   8, 0),      # Пусто
    ('NOMER_GTD', 'C',   6, 0),      # Пусто
    ('PR_SP',     'N',   1, 0),      # Пусто
    ('NAPRAVL',   'C',   1, 0),      # Пусто
    ('TYPE_DCL',  'C',   2, 0),      # Пусто
    ('DO53_GA',   'C',  14, 0),      # Пусто
    ('DO53_DATE', 'C',   8, 0),      # Пусто
    ('DO53_REG',  'C',  18, 0),      # Пусто
    ('NOM_REG',   'C',  18, 0),      # Пусто
    ('GA',        'C',  14, 0),      # Пусто
    ('GD1',       'C',   8, 0),      # Пусто
    ('GA_TIME',   'C',   8, 0),      # Пусто
    ('REG_TIME',  'C',   8, 0),      # Пусто
    ('GP1',       'C',   4, 0),      # Пусто
    ('G012_1',    'C',   4, 0),      # Пусто
    ('NAMEECP',   'C',  32, 0),      # Пусто
]


def generate_prihod_decl_dbf(
    clearance_invoice_id: int,
    output_path: str,
    encoding: str = 'cp866'
) -> None:
    """
    Generate a PRIHOD_DECL-format DBF file for a given ClearanceInvoice.

    One row per unique Declaration referenced by the invoice items.
    Schema defined by PRIHOD_DECL_FIELDS.

    Args:
        clearance_invoice_id (int): PK of the ClearanceInvoice.
        output_path (str): Full file path where the .dbf should be written.
        encoding (str, optional): Code page for the DBF. Defaults to 'cp866'.

    Raises:
        ValueError: If no ClearanceInvoice with the given ID exists.
        ValueError: If an unsupported field type is found in PRIHOD_DECL_FIELDS.
        OSError: If file deletion or writing fails.
    """
    logger.info(f"Starting PRIHOD_DECL DBF generation for invoice id={clearance_invoice_id}")

    # 1. Fetch invoice or error out early
    try:
        invoice = ClearanceInvoice.objects.get(pk=clearance_invoice_id)
        logger.info(f"Fetched ClearanceInvoice id={clearance_invoice_id}")
    except ClearanceInvoice.DoesNotExist:
        logger.error(f"ClearanceInvoice id={clearance_invoice_id} not found")
        raise ValueError(f"ClearanceInvoice with id={clearance_invoice_id} not found")

    # 2. Build DBF table spec string
    specs = []
    for name, ftype, length, dec in PRIHOD_DECL_FIELDS:
        if ftype == 'C':
            specs.append(f"{name} C({length})")
        elif ftype == 'N':
            specs.append(f"{name} N({length},{dec})")
        elif ftype == 'L':
            specs.append(f"{name} L")
        elif ftype == 'D':
            specs.append(f"{name} D")
        else:
            logger.error(f"Unsupported field type {ftype!r} in PRIHOD_DECL_FIELDS")
            raise ValueError(f"Unsupported field type {ftype!r} in PRIHOD_DECL_FIELDS")
    spec_line = "; ".join(specs)
    logger.debug(f"DBF spec line built: {spec_line}")

    # 3. Clean up existing file
    if os.path.exists(output_path):
        os.remove(output_path)
        logger.info(f"Removed existing file at {output_path}")

    # 4. Open DBF table for writing
    try:
        table = dbf.Table(output_path, spec_line, codepage=encoding)
        table.open(dbf.READ_WRITE)
        logger.info(f"Opened DBF table at {output_path}")
    except Exception as e:
        logger.exception(f"Failed to open DBF table at {output_path}: {e}")
        raise

    # 5. Fetch all related Declarations via invoice items
    items = (
        ClearedItem.objects
        .filter(clearance_invoice_id=invoice.id)
    )

    # Unique declarations
    decl_map = {}
    for item in items:
        decl = item.declared_item_id.declaration
        if decl and decl.pk not in decl_map:
            decl_map[decl.pk] = decl
    declarations = list(decl_map.values())
    logger.info(f"Found {len(declarations)} unique declarations for invoice id={clearance_invoice_id}")

    # 6. Populate rows inside a transaction
    row_count = 0
    with transaction.atomic():
        for decl in declarations:
            num = decl.declaration_number.replace('/', '')
            dop_nomer = f"d{num[:7]}"
            nomer_gtd = f"{num[5]}{num[-5:]}"

            row = {}
            for name, ftype, *_ in PRIHOD_DECL_FIELDS:
                if name == 'G549':
                    value = decl.declaration_number
                elif name == 'G013':
                    value = '7'
                elif name in ('G022', 'G082'):
                    value = decl.sender or ''
                elif name == 'G141':
                    value = '300031652'
                elif name == 'G142':
                    value = 'РУПП "ВИТЯЗЬ"'
                elif name == 'G143':
                    value = 'РБ, 210605, Г.ВИТЕБСК, УЛ.П.БРОВКИ 13А'
                elif name == 'G542':
                    value = decl.declaration_date
                elif name == 'DOP_NOMER':
                    value = dop_nomer
                elif name == 'NOMER_GTD':
                    value = nomer_gtd
                else:
                    # empty for all other fields
                    if ftype == 'C':
                        value = ''
                    else:
                        value = None
                row[name] = value

            table.append(row)
            row_count += 1

    logger.info(f"Inserted {row_count} rows into DBF")

    # 7. Close the table
    table.close()
    logger.info(f"Closed DBF table. PRIHOD_DECL.dbf written to {output_path}")