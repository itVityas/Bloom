from django.db import models


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
    production_code_id = models.IntegerField(blank=True, null=True)
    model_id = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=18, blank=True, null=True)
    color_id = models.CharField(max_length=4, blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    shift = models.CharField(max_length=3, blank=True, null=True)
    assembly_date_from = models.DateField(blank=True, null=True)
    assembly_date_to = models.DateField(blank=True, null=True)
    pakaging_date_from = models.DateField(blank=True, null=True)
    pakaging_date_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    apply_to_belarus = models.BooleanField()

    class Meta:
        ordering = ['-id']
