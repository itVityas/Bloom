# Generated by Django 4.2.23 on 2025-07-24 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_warehousedo_remove_warehouseproducthistory_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouseproduct',
            name='user',
        ),
    ]
