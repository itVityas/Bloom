# Generated by Django 4.2.20 on 2025-05-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sez', '0006_clearanceinvoiceitems_model_unv'),
    ]

    operations = [

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE sez_clearanceinvoiceitems "
                        "ADD CONSTRAINT fk_sez_clearanceinvoiceitems_model_name "
                        "FOREIGN KEY (model_name_id) REFERENCES model_names(id);"
                    ),
                    reverse_sql=(
                        "ALTER TABLE sez_clearanceinvoiceitems "
                        "DROP CONSTRAINT fk_sez_clearanceinvoiceitems_model_name;"
                    ),
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='clearanceinvoiceitems',
                    name='model_name',
                    field=models.ForeignKey(
                        to='shtrih.ModelNames',
                        on_delete=models.SET_NULL,
                        null=True,
                        blank=True,
                        related_name='clearance_invoice_items',
                        db_column='model_name_id',
                    ),
                ),
            ],
        ),
    ]
