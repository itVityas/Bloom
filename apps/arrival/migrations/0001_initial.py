# Generated by Django 4.2.20 on 2025-03-11 11:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClearanceInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('cleared', models.BooleanField()),
                ('ttn', models.CharField(blank=True, max_length=20, null=True)),
                ('series', models.CharField(blank=True, max_length=10, null=True)),
                ('recipient', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity_shipped', models.IntegerField(default=0)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('date_cleared', models.DateField(blank=True, null=True)),
                ('date_payments', models.DateTimeField()),
                ('date_calc', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClearanceInvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField()),
                ('model_name', models.CharField(blank=True, max_length=20, null=True)),
                ('model_code', models.CharField(blank=True, max_length=10, null=True)),
                ('quantity', models.FloatField()),
                ('actual_quantity', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('suppose_date', models.DateField()),
                ('exit_date', models.DateField()),
                ('delivery', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(default='Created', max_length=20)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shot_name', models.CharField(max_length=30)),
                ('count', models.PositiveIntegerField()),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='arrival.container')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='container',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='containers', to='arrival.order'),
        ),
        migrations.CreateModel(
            name='ClearedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('clearance_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cleared_items', to='arrival.clearanceinvoice')),
            ],
        ),
    ]
