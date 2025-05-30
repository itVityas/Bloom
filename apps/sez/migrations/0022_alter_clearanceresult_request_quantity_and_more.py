# Generated by Django 4.2.20 on 2025-05-26 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sez', '0021_clearanceresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clearanceresult',
            name='request_quantity',
            field=models.DecimalField(decimal_places=4, max_digits=19),
        ),
        migrations.AlterField(
            model_name='clearanceresult',
            name='uncleared_quantity',
            field=models.DecimalField(decimal_places=4, max_digits=19),
        ),
    ]
