from rest_framework.exceptions import ValidationError


class InvoiceNotFoundException(ValidationError):
    default_detail = 'Clearance invoice not found'
