
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
