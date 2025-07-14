from django.db import models

from apps.shtrih.models import Products
from apps.account.models import User


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class TypeOfWork(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class WarehouseAction(models.Model):
    name = models.CharField(max_length=100)
    type_of_work = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE)

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
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        db_constraint=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    warehouse_action = models.ForeignKey(
        WarehouseAction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    ttn_number = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Palleting(models.Model):
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE)
    warehouse_product = models.ForeignKey(
        WarehouseProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.pallet}:{self.warehouse_product}'
