from django.db import models

from apps.arrival.models import Container, Lot


class TrainDoc(models.Model):
    """
    Model representing a train document.
    Each train document is associated with an order and contains details about the document.
    """
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='invoices/', null=True, blank=True)
    sheet_count = models.IntegerField(default=0)
    prev_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)  # Date create of the invoice
    update_date = models.DateTimeField(auto_now=True)  # Date update of the invoice

    def __str__(self):
        return f"TrainDoc for Order: id:{self.id} order_id:{self.lot.id}"

    class Meta:
        ordering = ['-id']  # Order TrainDoc by date in descending order


class InvoiceContainer(models.Model):
    """
    Model representing an invoice.
    Each invoice is associated with a contract and contains details about the transaction.
    """
    number = models.CharField(max_length=15)  # Invoice number
    date = models.DateField()  # Date of the invoice
    sheet = models.CharField(max_length=50, blank=True, null=True)  # Excel sheet name
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True, blank=True
    )  # Associated container (optional)

    class Meta:
        ordering = ['-id']  # Order invoices by date in descending order

    def __str__(self):
        return f"Invoice {self.number} (Contract: {self.contract})"
