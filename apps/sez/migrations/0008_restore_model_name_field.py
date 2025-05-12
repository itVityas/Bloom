# apps/sez/migrations/0008_restore_model_name_field.py

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('sez', '0007_fix_model_name_fk'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # Никаких операций в БД — всё уже на месте
            database_operations=[],
            state_operations=[
                # 1) переименовываем IntegerField → model_name
                migrations.RenameField(
                    model_name='clearanceinvoiceitems',
                    old_name='model_name_id',
                    new_name='model_name',
                ),
                # 2) «Апгрейдим» тип поля из IntegerField в ForeignKey
                migrations.AlterField(
                    model_name='clearanceinvoiceitems',
                    name='model_name',
                    field=models.ForeignKey(
                        to='shtrih.ModelNames',
                        on_delete=django.db.models.deletion.SET_NULL,
                        null=True,
                        blank=True,
                        related_name='clearance_invoice_items',
                        db_column='model_name_id',
                    ),
                ),
            ],
        ),
    ]
