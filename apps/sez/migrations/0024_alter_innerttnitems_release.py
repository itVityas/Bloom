# Generated by Django 4.2 on 2025-05-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sez', '0023_merge_20250526_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innerttnitems',
            name='release',
            field=models.BooleanField(default=False),
        ),
    ]
