from django.db import models
from datetime import datetime


class ClearanceInvoice(models.Model):
    count = models.IntegerField()
    cleared = models.BooleanField()
    ttn = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=10, blank=True, null=True)
    recipient = models.CharField(max_length=100, blank=True, null=True)
    quantity_shipped = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=datetime.now)
    date_cleared = models.DateField(blank=True, null=True)
    date_payments = models.DateTimeField(blank=True, null=True)
    date_calc = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"ClearanceInvoice #{self.pk}"

    class Meta:
        ordering = ['id']


class ClearanceInvoiceItems(models.Model):
    clearance_invoice = models.ForeignKey(
        ClearanceInvoice,
        on_delete=models.CASCADE,
        related_name='clearance_invoice_items',
    )
    model_name = models.ForeignKey(
        'shtrih.ModelNames',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clearance_invoice_items',
        db_column='model_name_id',
    )
    declared_item = models.ForeignKey(
        'declaration.DeclaredItem',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clearance_invoice_items',
    )
    quantity = models.FloatField()
    model_unv = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"InvoiceItem #{self.pk} (Invoice #{self.clearance_invoice_id})"

    class Meta:
        ordering = ['id']


class ClearedItem(models.Model):
    product_id = models.IntegerField(
        null=True,
        blank=True,
    )
    clearance_invoice = models.ForeignKey(
        ClearanceInvoice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cleared_items'
    )
    declared_item_id = models.ForeignKey(
        'declaration.DeclaredItem',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cleared_items',
    )
    quantity = models.FloatField()

    def __str__(self):
        return f"ClearedItem #{self.pk} (Invoice #{self.clearance_invoice_id})"
