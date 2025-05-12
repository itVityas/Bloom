# apps/sez/migrations/0008_restore_model_name_field.py

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('sez', '0007_fix_model_name_fk'),
    ]

    operations = [
        # 1) Добавляем в БД обратно колонку model_name_id INT NULL
        # 2) Вешаем на неё FK к model_names(id)
        migrations.RunSQL(
            sql="""
                ALTER TABLE sez_clearanceinvoiceitems
                ADD model_name_id INT NULL;

                ALTER TABLE sez_clearanceinvoiceitems
                ADD CONSTRAINT fk_sez_clearanceinvoiceitems_model_name
                    FOREIGN KEY (model_name_id) REFERENCES model_names(id);
            """,
            reverse_sql="""
                ALTER TABLE sez_clearanceinvoiceitems
                DROP CONSTRAINT fk_sez_clearanceinvoiceitems_model_name;

                ALTER TABLE sez_clearanceinvoiceitems
                DROP COLUMN model_name_id;
            """,
        ),
    ]
