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
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'Not enough products for clearance'
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
    def __init__(self, detail=None, code=None):
        if not detail:
            detail = 'No panel component find in tv'
        self.detail = detail
        self.code = code

    def __str__(self):
        return self.detail
