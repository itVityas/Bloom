# Generated by Django 4.2 on 2025-03-10 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arrival', '0003_clearanceinvoice_date_calc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='invoice',
        ),
    ]
