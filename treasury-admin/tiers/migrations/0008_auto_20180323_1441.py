# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-23 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0007_tiersctrl_tiers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientctrl',
            name='nature',
        ),
        migrations.AddField(
            model_name='clientctrl',
            name='tiers',
            field=models.BooleanField(default=False, verbose_name='Tiers'),
        ),
        migrations.AlterModelTable(
            name='tiersctrl',
            table='THIRD_TIERS_CTRL',
        ),
    ]
