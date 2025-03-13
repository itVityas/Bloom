# Generated by Django 4.2.20 on 2025-03-11 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('arrival', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_code', models.CharField(max_length=3)),
                ('type', models.CharField(max_length=3)),
                ('sender', models.CharField(max_length=38)),
                ('sender_address', models.CharField(max_length=250)),
                ('delivery_terms', models.CharField(max_length=3)),
                ('item_count', models.IntegerField()),
                ('receiver', models.CharField(max_length=38)),
                ('receiver_address', models.CharField(max_length=250)),
                ('sender_country_code', models.CharField(max_length=3)),
                ('sender_alpha_country_code', models.CharField(max_length=2)),
                ('g15A_1', models.CharField(max_length=4)),
                ('payment_currency_code', models.CharField(max_length=3)),
                ('total_cost', models.DecimalField(decimal_places=4, max_digits=19)),
                ('currency_rate', models.DecimalField(decimal_places=4, max_digits=19)),
                ('foreign_economic_code', models.CharField(max_length=2)),
                ('payment_type_code', models.CharField(max_length=3)),
                ('provision_date', models.DateField()),
                ('paid_payment_details_count', models.SmallIntegerField()),
                ('declaration_id', models.IntegerField(unique=True)),
                ('declaration_number', models.CharField(max_length=18)),
                ('permit_number', models.CharField(max_length=23)),
                ('country_name', models.CharField(max_length=17)),
                ('declarant_position', models.CharField(max_length=250)),
                ('declarant_FIO', models.CharField(max_length=250)),
                ('document_id', models.CharField(max_length=36)),
                ('sender_country_name', models.CharField(max_length=17)),
                ('outgoing_number', models.CharField(max_length=50)),
                ('dollar_rate', models.DecimalField(decimal_places=4, max_digits=19)),
                ('euro_rate', models.DecimalField(decimal_places=4, max_digits=19)),
                ('declaration_date', models.DateField()),
                ('permit_code', models.CharField(max_length=3)),
                ('container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='declarations', to='arrival.container')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DeclaredItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('ordinal_number', models.IntegerField()),
                ('country_code', models.CharField(max_length=3)),
                ('alpha_country_code', models.CharField(max_length=3)),
                ('gross_weight', models.FloatField()),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('unit_code', models.CharField(blank=True, max_length=10, null=True)),
                ('unit_name', models.CharField(blank=True, max_length=20, null=True)),
                ('cost', models.DecimalField(decimal_places=4, max_digits=19)),
                ('statistical_cost', models.DecimalField(decimal_places=4, max_digits=19)),
                ('payment_details_count', models.IntegerField()),
                ('document_details_count', models.IntegerField()),
                ('code', models.CharField(max_length=50)),
                ('country_name', models.CharField(max_length=17)),
                ('g37', models.CharField(max_length=2)),
                ('net_weight', models.FloatField()),
                ('previous_customs_regime_code', models.CharField(max_length=2)),
                ('g373', models.CharField(max_length=3)),
                ('customs_cost', models.DecimalField(decimal_places=4, max_digits=19)),
                ('g31stz', models.CharField(max_length=50)),
                ('g311stz', models.CharField(max_length=3)),
                ('g312STZ', models.CharField(max_length=13)),
                ('valuation_method', models.CharField(max_length=2)),
                ('declaration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declared_items', to='declaration.declaration')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
