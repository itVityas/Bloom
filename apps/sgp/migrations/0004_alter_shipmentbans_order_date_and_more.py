# Generated by Django 4.2 on 2025-04-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgp', '0003_remove_shipmentbans_color_code_shipmentbans_color_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentbans',
            name='order_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='shipmentbans',
            name='order_number',
            field=models.CharField(max_length=10),
        ),
    ]
