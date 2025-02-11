# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-08 09:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import util.fileStorage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('util', '0008_catalog_type_product'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlowDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('nature', models.IntegerField(choices=[(0, 'CF_InFlow'), (1, 'CF_OutFlow')], default=1)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('date_val', models.DateField(blank=True, null=True)),
                ('montant', models.FloatField(blank=True, null=True)),
                ('chk_verify', models.BooleanField(default=False)),
                ('ref_id', models.CharField(blank=True, max_length=50, null=True)),
                ('chk_pay', models.BooleanField(default=False)),
                ('date_pay', models.DateField(blank=True, null=True)),
                ('obs', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('date_val', 'content_type', 'object_id'),
                'db_table': 'TRESOR_CASHFLOW_DETAIL',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CashFlowFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('date_update', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=util.fileStorage.models.upload_path_handler)),
                ('obs', models.CharField(blank=True, max_length=200, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('nature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='util.Catalog_Type_Doc')),
                ('oper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CREDIT_CTRL_FILE',
                'managed': True,
            },
        ),
    ]
