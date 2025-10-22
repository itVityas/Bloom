from django.db import models
from datetime import datetime

from apps.shtrih.models import ModelNames
from apps.arrival.models import Order


class ClearanceInvoice(models.Model):
    """
    Model representing a clearance invoice document.

    Tracks customs clearance information including:
    - Invoice identification (series/number)
    - Shipment details
    - Payment and calculation dates
    - Clearance status
    """
    count = models.IntegerField()
    cleared = models.BooleanField()
    ttn = models.CharField(max_length=20, blank=True, null=True)
    series = models.CharField(max_length=10, blank=True, null=True)
    recipient = models.CharField(max_length=100, blank=True, null=True)
    quantity_shipped = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=datetime.now)
    date_payments = models.DateTimeField(blank=True, null=True)
    date_calc = models.DateTimeField(blank=True, null=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_gifted = models.BooleanField(default=False)
    only_panel = models.BooleanField(default=False)

    def __str__(self):
        return f"ClearanceInvoice #{self.pk}"

    class Meta:
        ordering = ['id']


class ClearanceInvoiceItems(models.Model):
    """
    Line items within a clearance invoice.

    Contains details about specific products being cleared through customs.
    """
    clearance_invoice = models.ForeignKey(
        ClearanceInvoice,
        on_delete=models.CASCADE,
        related_name='clearance_invoice_items',
    )
    model_name_id = models.ForeignKey(
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

    def __str__(self):
        return f"InvoiceItem #{self.pk} (Invoice #{self.clearance_invoice_id})"

    class Meta:
        ordering = ['id']


class ClearedItem(models.Model):
    """
    clearance items than are cleared and they declaration
    """
    clearance_invoice_items = models.ForeignKey(
        ClearanceInvoiceItems,
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

    class Meta:
        ordering = ['id']


class InnerTTN(models.Model):
    """
    Internal Transport Transfer Note (TTN) document.

    Tracks internal product movements between locations.
    """
    car = models.CharField(max_length=100, blank=True, null=True)
    trailer = models.CharField(max_length=100, blank=True, null=True)
    waybill = models.CharField(max_length=100, blank=True, null=True)
    driver = models.CharField(max_length=100, blank=True, null=True)
    uuid = models.CharField(max_length=20, blank=True, null=True)
    shipper_unp = models.CharField(max_length=20)  # УНП грузоотправителя
    consignee_unp = models.CharField(max_length=20)  # УНП грузополучателя
    customer_unp = models.CharField(max_length=20)  # УНП плательщика
    customer = models.CharField(max_length=200)  # Плательщик
    shipper = models.CharField(max_length=200)  # грузоотправитель
    consignee = models.CharField(max_length=200)  # грузополучатель
    document = models.CharField(max_length=200)  # Документ, основание отпуска
    load = models.CharField(max_length=200)  # Пункт погрузки
    unload = models.CharField(max_length=200)  # Пункт выгрузки
    date = models.DateField()  # Дата документа
    notice = models.CharField(max_length=200)  # Примечание
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.uuid = f"R{self.id}"
            return self.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"InnerTTN #{self.pk}"

    class Meta:
        ordering = ['-id']


class InnerTTNItems(models.Model):
    """
    Line items within an internal transport document.

    Contains details about specific products being transported.
    """
    inner_ttn = models.ForeignKey(InnerTTN, on_delete=models.CASCADE)
    model_name = models.ForeignKey(ModelNames,
                                   on_delete=models.CASCADE,
                                   db_constraint=False,)
    measure = models.CharField(max_length=10)  # Единица измерения
    quantity = models.IntegerField()  # Количество
    price_pcs = models.DecimalField(max_digits=19, decimal_places=2)  # цена за единицу
    weight = models.DecimalField(max_digits=19, decimal_places=3)  # Вес
    nds = models.PositiveIntegerField(default=0)  # % ндс
    release = models.BooleanField(default=False)  # Реализация
    notice = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"InnerTTNItem #{self.pk} (InnerTTN #{self.inner_ttn_id})"

    class Meta:
        ordering = ['id']


class ClearanceUncleared(models.Model):
    """
    Tracks results of customs clearance attempts.

    Records failed clearance attempts with reasons.
    """
    invoice_item = models.ForeignKey(
        'ClearanceInvoiceItems',
        on_delete=models.CASCADE,
        related_name='clearance_results'
    )
    name = models.CharField(max_length=255)
    request_quantity = models.DecimalField(max_digits=19, decimal_places=4)
    uncleared_quantity = models.DecimalField(max_digits=19, decimal_places=4)
    reason = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Результат полной очистки'
        verbose_name_plural = 'Результаты полной очистки'

    def __str__(self):
        return f'{self.invoice_item} – {self.name}'
