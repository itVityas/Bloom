from django.db import models

from apps.arrival.models import Container


class Invoice(models.Model):
    """
    Model representing an invoice.
    Each invoice is associated with a contract and contains details about the transaction.
    """
    contract = models.CharField(max_length=100)  # Contract number or identifier
    number = models.CharField(max_length=10)  # Invoice number
    date = models.DateField()  # Date of the invoice
    recipient = models.CharField(max_length=200)  # Recipient of the invoice
    shipper = models.CharField(max_length=200, blank=True, null=True)  # Shipper (optional)
    seller = models.CharField(max_length=200, blank=True, null=True)  # Seller (optional)
    buyer = models.CharField(max_length=200)  # Buyer of the goods
    terms = models.CharField(max_length=50)  # Payment or delivery terms
    country = models.CharField(max_length=50)  # Country of origin or destination
    station = models.CharField(max_length=50)  # Station or location
    pto = models.CharField(max_length=150, null=True, blank=True)  # Port of Transit (optional)
    currency = models.CharField(max_length=3, default='USD')  # Currency code (e.g., USD, EUR)
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True, blank=True
    )  # Associated container (optional)


class InvoiceItem(models.Model):
    """
    Model representing an item within an invoice.
    Each item belongs to an invoice and contains details about the product.
    """
    code = models.CharField(max_length=30)  # Product code or SKU
    country = models.CharField(max_length=50)  # Country of origin for the item
    description_en = models.CharField(max_length=200)  # Description in English
    description_ru = models.CharField(max_length=200)  # Description in Russian
    measurements = models.CharField(max_length=20)  # Unit of measurement (e.g., kg, liters)
    quantity = models.IntegerField()  # Quantity of the item
    packages = models.IntegerField()  # Number of packages
    net_weight = models.DecimalField(max_digits=10, decimal_places=2)  # Net weight of the item
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2)  # Gross weight of the item
    price_pcs = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    price_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Total price for the item
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)  # Associated invoice
