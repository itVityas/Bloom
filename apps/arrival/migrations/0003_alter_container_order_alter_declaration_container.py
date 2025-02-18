# Generated by Django 4.2 on 2025-02-18 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arrival', '0002_remove_declaration_order_declaration_container'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='arrival.order'),
        ),
        migrations.AlterField(
            model_name='declaration',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='container', to='arrival.container'),
        ),
    ]
