# Generated by Django 4.2 on 2025-06-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrival', '0013_order_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
