# Generated by Django 4.2 on 2025-03-21 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sez', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clearanceinvoice',
            name='date_payments',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
