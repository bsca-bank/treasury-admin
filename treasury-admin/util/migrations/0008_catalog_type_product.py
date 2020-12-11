# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-30 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0007_catalog_type_doc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog_Type_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_l1', models.CharField(max_length=100)),
                ('category_l2', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Contr\xf4le de nomenclature produit',
                'db_table': 'UTIL_CATALOG_TYPE_PRODUCT',
                'managed': True,
                'verbose_name_plural': 'Contr\xf4le de nomenclature produit',
            },
        ),
    ]
