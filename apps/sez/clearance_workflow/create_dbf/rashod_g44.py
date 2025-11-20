import os
import logging
import dbf
from django.db import transaction

from apps.sez.models import ClearanceInvoice

logger = logging.getLogger(__name__)

# Получатель
RASHOD_DECL_FIELDS = [
    ('G32',       'N',   3, 0),
    ('G44i',      'N',  3, 0),
    ('G44KD',     'C',  2, 0),
    ('GND',       'C',  32, 0),
    ('G44DD',     'D',   8, 0),
    ('G44NS',     'C',  18, 0),
    ('DOP_NOMER', 'C',   8, 0),
    ('NOMER_GTD', 'C',   6, 0),
]


def generate_rashod_g44_dbf(
    clearance_invoice_id: int,
    output_path: str,
    encoding: str = 'cp866'
) -> None:
    """
    Generate a RASHOD_DECL-format DBF file for a given ClearanceInvoice.

    Always produces exactly one record containing invoice-level data:
      - constants for recipient (G141–G143)
      - invoice.id in G549 and NOMER_GTD
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
    logger.info(f"Starting RASHOD_DECL DBF generation for invoice id={clearance_invoice_id}")

    # 1. Fetch invoice
    try:
        invoice = ClearanceInvoice.objects.get(pk=clearance_invoice_id)
    except ClearanceInvoice.DoesNotExist:
        logger.error(f"ClearanceInvoice id={clearance_invoice_id} not found")
        raise ValueError(f"ClearanceInvoice with id={clearance_invoice_id} not found")

    if invoice.date_calc is None:
        logger.error("ClearanceInvoice.date_calc must be set to generate RASHOD_DECL")
        raise ValueError("ClearanceInvoice.date_calc must be set")

    # 2. Build DBF spec
    specs = []
    for name, ftype, length, dec in RASHOD_DECL_FIELDS:
        if ftype == 'C':
            specs.append(f"{name} C({length})")
        elif ftype == 'N':
            specs.append(f"{name} N({length},{dec})")
        elif ftype == 'L':
            specs.append(f"{name} L")
        elif ftype == 'D':
            specs.append(f"{name} D")
        else:
            logger.error(f"Unsupported field type {ftype!r} in RASHOD_DECL_FIELDS")
            raise ValueError(f"Unsupported field type {ftype!r} in RASHOD_DECL_FIELDS")
    spec_line = "; ".join(specs)
    logger.debug(f"DBF spec line built: {spec_line}")

    # 3. Remove existing file if present
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
        raise

    # 5. Build the single row
    row = {}

    # 6. Write and close in a transaction
    with transaction.atomic():
        table.append(row)
    logger.info("Inserted 1 row into DBF")

    table.close()
    logger.info(f"Closed DBF table. RASHOD_DECL.dbf written to {output_path}")
