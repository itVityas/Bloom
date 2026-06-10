from django.db import models

from apps.shtrih.models import Products
from apps.account.models import User
from apps.onec.models import OneCTTN


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class TypeOfWork(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}:{self.name}'


class WarehouseAction(models.Model):
    name = models.CharField(max_length=100)
    type_of_work = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE)
    operation = models.CharField(max_length=2, default='+')
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str(self):
        return f'{self.id}:{self.name}'


class WarehouseTTN(models.Model):
    ttn_number = models.CharField(max_length=50, primary_key=True)
    is_close = models.BooleanField(default=False)
    date = models. DateField(null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    warehouse_action = models.ForeignKey(WarehouseAction, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    onec_ttn = models.ForeignKey(OneCTTN, on_delete=models.PROTECT, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ttn_number']

    def __str__(self):
        return f'{self.ttn_number}'


class Pallet(models.Model):
    ttn_number = models.ForeignKey(WarehouseTTN, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}:{self.barcode}'


class OldProduct(models.Model):
    """
    Individual old_product items with barcodes, colors, and inventory information.
    """
    barcode = models.CharField(max_length=18)
    color_id = models.ForeignKey(
        'shtrih.Colors',
        on_delete=models.CASCADE,
        db_column='color_id',
        db_constraint=False,
        null=True,
        blank=True)
    model = models.ForeignKey('shtrih.Models', on_delete=models.CASCADE, db_column='model_id', db_constraint=False)
    state = models.IntegerField()
    quantity = models.IntegerField()
    is_shipment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"old_product {self.id} {self.barcode}"


class WarehouseDo(models.Model):
    warehouse_ttn = models.ForeignKey(WarehouseTTN, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, db_constraint=False, null=True, blank=True)
    old_product = models.ForeignKey(OldProduct, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'


class BarcodlessProducts(models.Model):
    model_name = models.ForeignKey('shtrih.ModelNames', on_delete=models.PROTECT, db_constraint=False)
    color = models.ForeignKey(
        'shtrih.Colors',
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        obj = BarcodlessProducts.objects.filter(
            model_name=self.model_name,
            color=self.color,
            warehouse=self.warehouse
        ).first()
        if obj:
            self.pk = obj.pk

        return super().save(*args, **kwargs)


class BarcodlessDo(models.Model):
    barcodless_product = models.ForeignKey(BarcodlessProducts, on_delete=models.PROTECT)
    warehouse_ttn = models.ForeignKey(WarehouseTTN, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        ttn = WarehouseTTN.objects.select_related('warehouse_action').filter(ttn_number=self.warehouse_ttn).first()
        barcodless_products = BarcodlessProducts.objects.filter(pk=self.barcodless_product_id).first()
        if not barcodless_products:
            raise Exception("Безштриховой товар не найден")
        if not ttn:
            raise Exception("ТТН не найдена")
        if ttn.is_close:
            raise Exception("ТТН закрыта")
        if ttn.warehouse_action.operation == '+':
            barcodless_products.quantity += self.quantity
        elif ttn.warehouse_action.operation == '-':
            if barcodless_products.quantity < self.quantity:
                raise Exception("Недостаточно товара на складе")
            barcodless_products.quantity -= self.quantity
        barcodless_products.save()
        super().save(*args, **kwargs)


class NotPackaging(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_constraint=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    bloom_user = models.ForeignKey(User, on_delete=models.CASCADE)
    factory_user = models.ForeignKey(
        'shtrih.ShtrihUser',
        on_delete=models.CASCADE,
        db_constraint=False,
        null=True, blank=True)
    found_date = models.DateTimeField(auto_now_add=True)
    solve_date = models.DateTimeField(blank=True, null=True)
    is_solved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'
