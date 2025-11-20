import os
import logging
import dbf
from django.db import transaction
from django.db.models import Prefetch

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems, ClearedItem

logger = logging.getLogger(__name__)

# Field definitions for the NORM .dbf
NORM_FIELDS = [
    ('GTDGA_O',    'C', 16, 0),      # Порядковый номер, ClearanceInvoice.id
    ('TOVGTDNO_O', 'N', 11, 0),      # Порядковый номер модели в ClearanceInvoiceItems
    ('GTDGA',      'C', 50, 0),      # Номер декларации, Declaration.declaration_number
    ('TOVGTDNO',   'N', 11, 0),      # Номер товара в декларации, DeclaredItem.ordinal_number
    ('TOVCOUNT',   'C', 19, 2),      # Количество ClearedItem.quantity
    ('SUBCODE',    'C', 20, 0),      # Пусто
    ('TNVD',       'C', 10, 0),      # Пусто
    ('SUBCODE_O',  'C', 20, 0),      # Пусто
    ('TNVD_O',     'C', 10, 0),      # Пусто
    ('GTDGD',      'D',  8, 0),      # Пусто
]


def generate_norm_dbf(clearance_invoice_id: int, output_path: str, encoding: str = 'cp866') -> None:
    """
    Generate a NORM-format DBF file for a given ClearanceInvoice.

    The output .dbf will contain one row per ClearedItem across all items
    in the specified invoice. Schema defined by NORM_FIELDS.

    Args:
        clearance_invoice_id (int): PK of the ClearanceInvoice.
        output_path (str): Full file path where the .dbf should be written.
        encoding (str, optional): Code page for the DBF. Defaults to 'cp866'.

    Raises:
        ValueError: If no ClearanceInvoice with the given ID exists.
        ValueError: If an unsupported field type is found in NORM_FIELDS.
        OSError: If file deletion or writing fails.
    """
    logger.info(f"Starting NORM DBF generation for invoice id={clearance_invoice_id}")

    # 1. Fetch invoice or error out early
    try:
        invoice = ClearanceInvoice.objects.get(pk=clearance_invoice_id)
        logger.info(f"Fetched ClearanceInvoice id={clearance_invoice_id}")
    except ClearanceInvoice.DoesNotExist:
        logger.error(f"ClearanceInvoice id={clearance_invoice_id} not found")
        raise ValueError(f"ClearanceInvoice with id={clearance_invoice_id} not found")

    # 2. Build DBF table spec string
    specs = []
    for name, ftype, length, dec in NORM_FIELDS:
        if ftype == 'C':
            specs.append(f"{name} C({length})")
        elif ftype == 'N':
            specs.append(f"{name} N({length},{dec})")
        elif ftype == 'L':
            specs.append(f"{name} L")
        elif ftype == 'D':
            specs.append(f"{name} D")
        else:
            logger.error(f"Unsupported field type {ftype!r} in NORM_FIELDS")
            raise ValueError(f"Unsupported field type {ftype!r} in NORM_FIELDS")
    spec_line = "; ".join(specs)
    logger.debug(f"DBF spec line built: {spec_line}")

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

    # 5. Query invoice items and prefetch all related cleared items + declarations
    invoice_items = (
        ClearanceInvoiceItems.objects
        .filter(clearance_invoice_id=invoice.id)
        .prefetch_related(
            Prefetch(
                'cleared_items',
                queryset=ClearedItem.objects.select_related('declared_item_id__declaration'),
                to_attr='prefetched_cleared_items'
            )
        )
    )
    logger.info(f"Prefetching related items for invoice id={clearance_invoice_id}")

    # 6. Populate rows inside a transaction to ensure atomicity
    row_count = 0
    with transaction.atomic():
        for item_index, item in enumerate(invoice_items, start=1):
            for rec in getattr(item, 'prefetched_cleared_items', []):
                inv_str = str(invoice.id)
                value = inv_str[-6:].rjust(4, '0')
                row = {
                    'GTDGA_O':    value,
                    'TOVGTDNO_O': item_index,
                    'GTDGA':      rec.declared_item_id.declaration.declaration_number,
                    'TOVGTDNO':   rec.declared_item_id.ordinal_number,
                    'TOVCOUNT':   str(rec.quantity),
                    'SUBCODE':    '',
                    'TNVD':       '',
                    'SUBCODE_O':  '',
                    'TNVD_O':     '',
                    'GTDGD':      None,
                }
                table.append(row)
                row_count += 1
    logger.info(f"Inserted {row_count} rows into DBF")

    # 7. Close the table to flush to disk
    table.close()
    logger.info(f"Closed DBF table. NORM.dbf written to {output_path}")
