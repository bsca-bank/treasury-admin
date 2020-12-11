# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0008_catalog_type_product'),
        ('treasury', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fi',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Catalog_Type_Product'),
        ),
        migrations.AddField(
            model_name='fx',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Catalog_Type_Product'),
        ),
        migrations.AddField(
            model_name='mm',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Catalog_Type_Product'),
        ),
    ]
