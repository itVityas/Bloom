# Generated by Django 4.2 on 2025-04-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shtrih', '0003_modules'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_code', models.CharField(blank=True, db_column='color_code', max_length=4, null=True)),
                ('russian_title', models.CharField(blank=True, db_column='russian_title', max_length=50, null=True)),
            ],
            options={
                'db_table': 'colors',
                'ordering': ['id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Production_codes',
            fields=[
                ('code', models.IntegerField(db_column='code', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=70)),
                ('nameplate', models.BooleanField(db_column='nameplate')),
            ],
            options={
                'db_table': 'production_codes',
                'ordering': ['-code'],
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='consignments',
            options={'managed': False, 'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='modelnames',
            options={'managed': False, 'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='models',
            options={'managed': False, 'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='modules',
            options={'managed': False, 'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'managed': False, 'ordering': ['-id']},
        ),
    ]
