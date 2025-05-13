from django.db import models

from apps.shtrih.models import Production_codes, Colors, Modules, ModelNames


class StorageLimits(models.Model):
    """
    Model to store storage limits
    """
    max_storage_days = models.IntegerField()
    production_code = models.IntegerField()
    model_code = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-id']


class ShipmentBans(models.Model):
    """
    Model to store shipment bans
    """
    order_number = models.CharField(max_length=10)
    order_date = models.DateField()
    message = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    production_code_id = models.ForeignKey(
        Production_codes,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        db_constraint=False)
    model_name_id = models.ForeignKey(
        ModelNames,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        db_constraint=False)
    barcode = models.CharField(max_length=18, blank=True, null=True)
    color_id = models.ForeignKey(
        Colors,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        db_constraint=False)
    module_id = models.ForeignKey(
        Modules,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        db_constraint=False)
    shift = models.CharField(max_length=3, blank=True, null=True)
    assembly_date_from = models.DateField(blank=True, null=True)
    assembly_date_to = models.DateField(blank=True, null=True)
    pakaging_date_from = models.DateField(blank=True, null=True)
    pakaging_date_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    apply_to_belarus = models.BooleanField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        """Return the string representation of the Content."""
        return str(self.id)
