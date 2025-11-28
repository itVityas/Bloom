from rest_framework.exceptions import ValidationError


class InvoiceNotFoundException(ValidationError):
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'Clearance invoice not found'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class InvoiceAlreadyClearedException(ValidationError):
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'Clearance invoice already cleared'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class ProductsNotEnoughException(ValidationError):
    def __init__(self, have_count, req_count, model_name='', detail=None, code=None):
        if not detail:
            detail = f'''Недостаточно товаров для списания.
Для модели {model_name} доступно {have_count} из {req_count}
Решение: 1. Измените количество для списания в соответствии с фактическим количеством
2. Уточните фактическое количество выбитых штрихкодов на производстве
            '''
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class InternalException(ValidationError):
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'Internal error'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class OracleException(ValidationError):
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'Oracle error'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class PanelException(ValidationError):
    def __init__(self, model_name, order='', detail=None, code=None):
        if not detail:
            detail = f'''Панели для модели {model_name} не найдены в заказе {order}
Решение: Проверьте правильность заказа
            '''
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class TTNUsedException(ValidationError):
    def __init__(self, ttn_name, invoice_id='', detail=None, code=None):
        if not detail:
            detail = f'Накладная {ttn_name} уже использована в другом рассчете {invoice_id}'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class NoClearedItemException(ValidationError):
    def __init__(self, model_name, detail=None, code=None):
        if not detail:
            detail = f'Ничего не было растаможено для модели - {model_name}' +\
                '\nРешение: проверьте правильность заказа'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail


class NoMatchedTTNException(ValidationError):
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'ТТН была изменена, проверьте ТТН'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail
