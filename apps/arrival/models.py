from django.db import models
from datetime import datetime


class Order(models.Model):
    """
    Model representing an order.
    """
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Order."""
        return self.name


class Container(models.Model):
    """
    Model representing a container.
    """
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='containers'
    )
    name = models.CharField(max_length=30)
    suppose_date = models.DateField()
    load_date = models.DateField(blank=True, null=True)
    exit_date = models.DateField()
    delivery = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20, default="Created")
    notice = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Container."""
        return self.name


class Content(models.Model):
    """
    Model representing content associated with a container.
    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    count = models.PositiveIntegerField()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name='contents'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Content."""
        return self.shot_name


class ClearanceInvoice(models.Model):
    count = models.IntegerField()
    cleared = models.BooleanField()
    ttn = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=10, blank=True, null=True)
    recipient = models.CharField(max_length=100, blank=True, null=True)
    quantity_shipped = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=datetime.now)
    date_cleared = models.DateField(blank=True, null=True)
    date_payments = models.DateTimeField()
    date_calc = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"ClearanceInvoice #{self.pk}"


class ClearanceInvoiceItems(models.Model):
    clearance_invoice = models.ForeignKey(
        ClearanceInvoice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clearance_invoice_items',
    )
    model_id = models.IntegerField()
    model_name = models.CharField(max_length=20, blank=True, null=True)
    model_code = models.CharField(max_length=10, blank=True, null=True)
    declared_item = models.ForeignKey(
        'declaration.DeclaredItem',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clearance_invoice_items',
    )
    quantity = models.FloatField()
    actual_quantity = models.FloatField(default=0)

    def __str__(self):
        return f"InvoiceItem #{self.pk} (Invoice #{self.clearance_invoice_id})"


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
