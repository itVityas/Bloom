from django.db import models

from apps.shtrih.models import Products


class warehouse(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class type_of_work(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class warehouse_action(models.Model):
    name = models.CharField(max_length=100)
    type_of_work = models.ForeignKey(type_of_work, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str(self):
        return f'{self.id}:{self.name}'


class Pallet(models.Model):
    barcode = models.CharField(max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.barcode}'


class WarehouseProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(warehouse, on_delete=models.CASCADE)
    warehouse_action = models.ForeignKey(warehouse_action, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ttn_number = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Palleting(models.Model):
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE)
    warehouse_product = models.ForeignKey(WarehouseProduct, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.pallet}:{self.warehouse_product}'
