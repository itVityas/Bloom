from django.db import models


# Create your models here.
class ReportStorage(models.Model):
    """
CREATE VIEW report_storage AS
SELECT name.id as model_name_id, name.name as name,
    COUNT(CASE WHEN pr.cleared is null THEN 1 END) as uncleared,
    COUNT(CASE WHEN pr.cleared is not null AND invoice.recipient_id != 4 THEN 1 END) as cleared,
    COUNT(CASE WHEN pt.new_product_id is not null THEN 1 END) as simple,
    COUNT(CASE WHEN invoice.recipient_id=4 THEN 1 END) as compensation,
    wt.warehouse_id as warehouse_id
FROM products as pr
JOIN models as mod ON pr.model_id = mod.id
JOIN model_names as name ON mod.name_id = name.id
LEFT JOIN product_transitions as pt ON pr.id = pt.new_product_id
JOIN warehouse_warehouseproduct as wp ON wp.product_id = pr.id
JOIN warehouse_warehousedo wd ON wd.warehouse_product_id = wp.id
JOIN warehouse_warehousettn wt ON wt.ttn_number = wd.warehouse_ttn_id
JOIN protocols as prot ON prot.product_id = pr.id
JOIN invoices as invoice ON invoice.id = prot.invoice_id
where  (pr.state <> 1)
GROUP BY name.id, name.name, wt.warehouse_id
    """
    model_name_id = models.IntegerField(db_column='model_name_id', primary_key=True)
    name = models.CharField(max_length=255)
    uncleared = models.IntegerField()
    cleared = models.IntegerField()
    simple = models.IntegerField()
    compensation = models.IntegerField()
    warehouse_id = models.IntegerField(db_column='warehouse_id')

    class Meta:
        managed = False
        db_table = 'report_storage'
        ordering = ['model_name_id']
