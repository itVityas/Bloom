# Generated by Django 4.2 on 2025-05-20 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shtrih', '0005_modelcolors'),
        ('sez', '0016_remove_innerttnitems_item_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innerttnitems',
            name='model_name',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='shtrih.modelnames'),
        ),
    ]
