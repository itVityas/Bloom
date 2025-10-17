from rest_framework.exceptions import ValidationError


class InvoiceNotFoundException(ValidationError):
    default_detail = 'Clearance invoice not found'


class InvoiceAlreadyClearedException(ValidationError):
    default_detail = 'Clearance invoice already cleared'


class ProductsNotEnoughException(ValidationError):
    default_detail = 'Not enough products for clearance'


class InternalException(ValidationError):
    default_detail = 'Internal error'


class OracleException(ValidationError):
    default_detail = 'Oracle error'
