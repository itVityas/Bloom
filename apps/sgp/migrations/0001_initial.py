# Generated by Django 4.2 on 2025-03-26 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentBans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(blank=True, max_length=10, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('work_start_date', models.CharField(blank=True, max_length=10, null=True)),
                ('work_end_date', models.CharField(blank=True, max_length=10, null=True)),
                ('type_of_work_id', models.IntegerField(blank=True, null=True)),
                ('module_id', models.IntegerField(blank=True, null=True)),
                ('production_code', models.IntegerField(blank=True, null=True)),
                ('model_id', models.IntegerField(blank=True, null=True)),
                ('color_code', models.CharField(blank=True, max_length=4, null=True)),
                ('message', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('apply_to_belarus', models.BooleanField()),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='StorageLimits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_storage_days', models.IntegerField()),
                ('production_code', models.IntegerField()),
                ('model_code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
