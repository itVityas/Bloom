from rest_framework.exceptions import ValidationError


class InvoiceNotFoundException(ValidationError):
    default_detail = 'Clearance invoice not found'


class InvoiceAlreadyClearedException(ValidationError):
    default_detail = 'Clearance invoice already cleared'
