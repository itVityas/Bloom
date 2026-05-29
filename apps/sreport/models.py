from django.db import models

from apps.shtrih.models import Modules, Workplaces


# Create your models here.
class ReportStorage(models.Model):
    """
CREATE VIEW report_storage AS
SELECT name.id as model_name_id, name.name as name, COUNT(CASE WHEN pr.cleared is null THEN 1 END) as uncleared,
    COUNT(CASE WHEN pr.cleared is not null AND invoice.recipient_id != 4 THEN 1 END) as cleared,
    COUNT(CASE WHEN pt.new_product_id is not null THEN 1 END) as simple,
    COUNT(CASE WHEN invoice.recipient_id=4 THEN 1 END) as compensation,
    wt.warehouse_id as warehouse_id
FROM products as pr
JOIN models as mod ON pr.model_id = mod.id
JOIN model_names as name ON mod.name_id = name.id
LEFT JOIN product_transitions as pt ON pr.id = pt.new_product_id
JOIN warehouse_warehousedo wd ON wd.product_id = pr.id
JOIN warehouse_warehousettn wt ON wt.ttn_number = wd.warehouse_ttn_id
JOIN protocols as prot ON prot.product_id = pr.id
JOIN invoices as invoice ON invoice.id = prot.invoice_id
where  (pr.state <> 1 and wt.warehouse_id <> 12)
GROUP BY name.id, name.name, wt.warehouse_id
    """
    model_name_id = models.IntegerField(db_column='model_name_id', primary_key=True)
    name = models.CharField(max_length=255)
    uncleared = models.IntegerField()
    cleared = models.IntegerField()
    simple = models.IntegerField()
    compensation = models.IntegerField()
    warehouse_id = models.IntegerField(db_column='warehouse_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_storage'
        ordering = ['model_name_id']


class ProductPlan(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, db_constraint=False,)
    shift = models.CharField(max_length=1)
    workplace = models.ForeignKey(Workplaces, on_delete=models.CASCADE, db_constraint=False,)
    month_count = models.PositiveIntegerField()
    day_count = models.PositiveIntegerField()

    class Meta:
        ordering = ['module']
        # unique_together = ('module', 'shift')

    def save(self, *args, **kwargs):
        if ProductPlan.objects.filter(module=self.module, shift=self.shift, workplace=self.workplace).exists():
            ProductPlan.objects.filter(module=self.module, shift=self.shift, workplace=self.workplace).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.module} {self.shift}"


class OneCTTNItemScanedCount(models.Model):
    """
create view [dbo].[onec_onecttnitem_with_scanned_count]
as
SELECT
    onec_onecttnitem.id as 'one_C_ttn_item_id',
    onec_onecttn.number,
    onec_onecttn.series,
    model_names.id	 as 'model_name_id',
    model_names.name as 'full_name',
    products.color_id,
    colors.color_code,
    onec_onecttnitem.count,
    warehouse_warehousettn.warehouse_id as 'warehouse_warehouse_id',
    warehouse_warehouse.name as 'warehouse_name',
    count(distinct warehouse_warehousedo.id) as 'scanned'
FROM [bloomtest].[dbo].[onec_onecttn]
  join warehouse_warehousettn on warehouse_warehousettn.onec_ttn_id  = onec_onecttn.id
  join warehouse_warehousedo on warehouse_warehousettn.ttn_number = warehouse_warehousedo.warehouse_ttn_id
  join products on products.id = warehouse_warehousedo.product_id
  join models on models.id = products.model_id
  join onec_onecttnitem on onec_onecttnitem.onec_ttn_id = onec_onecttn.id and models.name_id = onec_onecttnitem.model_name_id
  join model_names on onec_onecttnitem.model_name_id = model_names.id
  left join colors on products.color_id = colors.id
  join warehouse_warehouse on warehouse_warehouse.id = warehouse_warehousettn.warehouse_id
where not exists(
    select top 1 * from warehouse_warehousedo as wd
    join warehouse_warehousettn as wt on wt.ttn_number = wd.warehouse_ttn_id
    join warehouse_warehouseaction as wa on wa.id = wt.warehouse_action_id
    where wd.product_id = warehouse_warehousedo.product_id and wa.type_of_work_id = 4
    )

group by onec_onecttnitem.id,
    onec_onecttn.number, onec_onecttn.series,
    model_names.id,
    model_names.name,
    products.color_id,
    onec_onecttnitem.count,
    colors.color_code,
    warehouse_warehousettn.warehouse_id,
    warehouse_warehouse.name
    """
    onec_ttn_item_id = models.BigIntegerField(db_column='one_C_ttn_item_id', primary_key=True, unique=False)
    onec_ttn_number = models.CharField(max_length=50, db_column='number')
    onec_ttn_series = models.CharField(max_length=50, db_column='series')
    model_name_id = models.IntegerField(db_column='model_name_id')
    full_name = models.CharField(max_length=100, db_column='full_name')
    color_id = models.IntegerField(db_column='color_id', null=True, blank=True)
    color_code = models.CharField(max_length=4, db_column='color_code', null=True, blank=True)
    count = models.IntegerField(db_column='count')
    warehouse_warehouse_id = models.BigIntegerField(db_column='warehouse_warehouse_id')
    warehouse_name = models.CharField(max_length=100, db_column='warehouse_name')
    scanned = models.IntegerField(db_column='scanned', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'onec_onecttnitem_with_scanned_count'
        ordering = ['onec_ttn_item_id']


class WarehouseTTNBarcode(models.Model):
    """
ALTER VIEW warehouse_ttn_barcode AS
SELECT pr.id as product_id, pr.barcode as product_barcode, us.id as user_id, us.fio as user_fio, mn.id as model_name_id, mn.name as model_name_name, wr.id as warehouse_id, wr.name as warehouse_name, do.create_at as warehouse_do_create_at, wt.ttn_number as warehouse_ttn_ttn_number, onec.number as onec_number, onec.series as onec_series
FROM dbo.products as pr
JOIN dbo.warehouse_warehousedo as do ON do.product_id = pr.id
JOIN dbo.warehouse_warehousettn as wt ON wt.ttn_number = do.warehouse_ttn_id
JOIN dbo.warehouse_warehouse as wr ON wr.id = wt.warehouse_id
JOIN dbo.account_user as us ON wt.user_id = us.id
JOIN dbo.onec_onecttn as onec ON onec.id = wt.onec_ttn_id
JOIN dbo.models as model ON model.id = pr.model_id
JOIN dbo.model_names as mn ON model.name_id = mn.id
    """
    product_id = models.IntegerField(db_column='product_id', primary_key=True)
    product_barcode = models.CharField(max_length=18, db_column='product_barcode')
    user_id = models.IntegerField(db_column='user_id')
    user_fio = models.CharField(max_length=255, db_column='user_fio', blank=True, null=True)
    model_name_id = models.IntegerField(db_column='model_name_id')
    model_name_name = models.CharField(max_length=100, db_column='model_name_name')
    warehouse_id = models.IntegerField(db_column='warehouse_id')
    warehouse_name = models.CharField(max_length=100, db_column='warehouse_name')
    warehouse_do_create_at = models.DateTimeField(db_column='warehouse_do_create_at')
    warehouse_ttn_ttn_number = models.CharField(max_length=50, db_column='warehouse_ttn_ttn_number')
    onec_number = models.CharField(max_length=50, db_column='onec_number')
    onec_series = models.CharField(max_length=50, db_column='onec_series')

    class Meta:
        managed = False
        db_table = 'warehouse_ttn_barcode'
        ordering = ['product_id']


class WarehouseMonthModelCount(models.Model):
    """
ALTER VIEW warehouse_month_count AS
SELECT
    names.id, names.name,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -1, GETDATE()) AND GETDATE() THEN prod.available_quantity ELSE 0 END) as month1,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -2, GETDATE()) AND DATEADD(month, -1, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month2,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -3, GETDATE()) AND DATEADD(month, -2, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month3,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -4, GETDATE()) AND DATEADD(month, -3, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month4,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -5, GETDATE()) AND DATEADD(month, -4, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month5,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -6, GETDATE()) AND DATEADD(month, -5, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month6,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -7, GETDATE()) AND DATEADD(month, -6, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month7,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -8, GETDATE()) AND DATEADD(month, -7, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month8,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -9, GETDATE()) AND DATEADD(month, -8, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month9,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -10, GETDATE()) AND DATEADD(month, -9, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month10,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -11, GETDATE()) AND DATEADD(month, -10, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month11,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -12, GETDATE()) AND DATEADD(month, -11, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month12,
    SUM(CASE WHEN ttn.date BETWEEN DATEADD(month, -24, GETDATE()) AND DATEADD(month, -12, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month24,
    SUM(CASE WHEN ttn.date < DATEADD(month, -24, GETDATE()) THEN prod.available_quantity ELSE 0 END) as month_more
FROM dbo.model_names AS names
JOIN dbo.models AS models ON models.name_id = names.id
JOIN dbo.products AS prod ON prod.model_id = models.id
JOIN dbo.warehouse_warehousedo AS do ON prod.id = do.product_id
JOIN dbo.warehouse_warehousettn AS ttn ON ttn.ttn_number = do.warehouse_ttn_id
WHERE ttn.onec_ttn_id IS null AND prod.available_quantity > 0
GROUP BY names.id, names.name
    """
    model_name = models.CharField(db_column='name', max_length=100)
    month1 = models.IntegerField(db_column='month1')
    month2 = models.IntegerField(db_column='month2')
    month3 = models.IntegerField(db_column='month3')
    month4 = models.IntegerField(db_column='month4')
    month5 = models.IntegerField(db_column='month5')
    month6 = models.IntegerField(db_column='month6')
    month7 = models.IntegerField(db_column='month7')
    month8 = models.IntegerField(db_column='month8')
    month9 = models.IntegerField(db_column='month9')
    month10 = models.IntegerField(db_column='month10')
    month11 = models.IntegerField(db_column='month11')
    month12 = models.IntegerField(db_column='month12')
    month24 = models.IntegerField(db_column='month24')
    month_more = models.IntegerField(db_column='month_more')

    class Meta:
        managed = False
        db_table = 'warehouse_month_count'
        ordering = ['id']
