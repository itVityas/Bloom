from rest_framework.exceptions import APIException


class ProductNotFound(APIException):
    status_code = 404
    default_detail = 'Product with this barcode does not exist'
    default_code = 'product_not_found'
