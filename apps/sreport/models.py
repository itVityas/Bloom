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
