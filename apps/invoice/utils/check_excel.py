from openpyxl import load_workbook


def find_sheet(invoice_number, container_name, file) -> str:
    try:
        wb = load_workbook(file)
        for sheet in wb.worksheets:
            container_check = False
            number_check = False
            for row in sheet.iter_rows(values_only=True, max_row=30):
                for cell in row:
                    if cell == container_name:
                        container_check = True
                    if cell == invoice_number:
                        number_check = True
                    if container_check and number_check:
                        return sheet.title
    except Exception as e:
        print(e)
    return None
