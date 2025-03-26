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
    order_number = models.CharField(max_length=10, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    work_start_date = models.CharField(max_length=10, blank=True, null=True)
    work_end_date = models.CharField(max_length=10, blank=True, null=True)
    type_of_work_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    production_code = models.IntegerField(blank=True, null=True)
    model_id = models.IntegerField(blank=True, null=True)
    color_code = models.CharField(max_length=4, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    apply_to_belarus = models.BooleanField()

    class Meta:
        ordering = ['-id']
