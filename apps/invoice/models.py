from django.db import models

from apps.arrival.models import Container, Order


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='invoices/')
    prev_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)  # Date create of the invoice
    update_date = models.DateTimeField(auto_now=True)  # Date update of the invoice

    def __str__(self):
        return f"Invoice for Order: id:{self.id} order_id:{self.order.id}"

    class Meta:
        ordering = ['-id']  # Order invoices by date in descending order


class InvoiceContainer(models.Model):
    """
    Model representing an invoice.
    Each invoice is associated with a contract and contains details about the transaction.
    """
    number = models.CharField(max_length=10)  # Invoice number
    date = models.DateField()  # Date of the invoice
    sheet = models.CharField(max_length=50, blank=True, null=True)  # Excel sheet name
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True, blank=True
    )  # Associated container (optional)

    class Meta:
        ordering = ['-id']  # Order invoices by date in descending order

    def __str__(self):
        return f"Invoice {self.number} (Contract: {self.contract})"
