# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-26 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0021_auto_20180324_1403'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientctrlfile',
            options={'managed': True, 'ordering': ('-date_val',), 'verbose_name': 'Ctrl Client (T\xe9l\xe9chargement)', 'verbose_name_plural': 'Ctrl Client (T\xe9l\xe9chargement)'},
        ),
    ]
