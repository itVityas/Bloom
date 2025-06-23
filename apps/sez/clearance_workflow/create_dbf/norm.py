import os
import datetime
import dbf
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.sez.models import ClearedItem

# Список товаров
NORM_FIELDS = [
    ('GTDGA_O',   'C', 16, 0),      # Порядковый номер, ClearanceInvoice.id
    ('TOVGTDNO_O','N', 11, 0),      # Порядковый номер модели в ClearanceInvoiceItems (Например есть 5 ClearanceInvoiceItems для ClearanceInvoice, нужно записать какой это по порядку 1,2,3,4,5)
    ('GTDGA',     'C', 50, 0),      # Номер декларации, Declaration.declaration_number
    ('TOVGTDNO',  'N', 11, 0),      # Номер товара в декларации, DeclaredItem.ordinal_number
    ('TOVCOUNT',  'C', 19, 0),      # Количество ClearedItem.quantity
    ('SUBCODE',   'C', 20, 0),      # Пусто
    ('TNVD',      'C', 10, 0),      # Пусто
    ('SUBCODE_O', 'C', 20, 0),      # Пусто
    ('TNVD_O',    'C', 10, 0),      # Пусто
    ('GTDGD',     'D',  8, 0),      # Пусто
]


def generate_norm_dbf(clearance_invoice_id: int, output_path: str, encoding: str = 'cp866') -> None:

    # 1. Получаем инвойс
    try:
        invoice = ClearanceInvoice.objects.get(pk=clearance_invoice_id)
    except ObjectDoesNotExist:
        raise ValueError(f"ClearanceInvoice с id={clearance_invoice_id} не найден")

    # 2. Готовим spec для dbf.Table
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
            raise ValueError(f"Unsupported field type {ftype!r} in NORM_FIELDS")
    spec_line = "; ".join(specs)

    # 3. Создаём/перезаписываем файл
    if os.path.exists(output_path):
        os.remove(output_path)
    table = dbf.Table(output_path, spec_line, codepage=encoding)
    table.open(dbf.READ_WRITE)

    # 4. Заполняем строки
    invoice_items = ClearanceInvoiceItems.objects.filter(clearance_invoice_id=clearance_invoice_id)

    with transaction.atomic():
        for idx, item in enumerate(invoice_items, start=1):
            print(item.declared_item)

            records = ClearedItem.objects.filter(
                clearance_invoice=item.clearance_invoice_id,
            )
            for record in records:
                print(record)

            for rec in records:
                # Строим словарь под одну запись
                row = {
                    'GTDGA_O':    str(invoice.id),
                    'TOVGTDNO_O': idx,
                    'GTDGA':      item.declared_item.declaration_id.declaration_number,
                    'TOVGTDNO':   item.declared_item.ordinal_number,
                    'TOVCOUNT':   str(rec['quantity']),
                    'SUBCODE':    '',
                    'TNVD':       '',
                    'SUBCODE_O':  '',
                    'TNVD_O':     '',
                    'GTDGD':      None,
                }
                table.append(row)

    # 5. Закрываем
    table.close()
    print(f"NORM.dbf успешно записан в {output_path}")
