# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 17:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0008_auto_20171009_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashflowfile',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cashflowfile',
            name='nature',
        ),
        migrations.RemoveField(
            model_name='cashflowfile',
            name='oper',
        ),
        migrations.DeleteModel(
            name='CashFlowFile',
        ),
    ]
