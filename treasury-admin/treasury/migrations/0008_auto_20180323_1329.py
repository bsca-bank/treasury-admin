# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-23 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0007_auto_20180323_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fx',
            name='client',
            field=models.ForeignKey(blank=True, help_text='Tapez le code client ici Amplitude', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fx_client', to='tiers.ClientCtrl', verbose_name='Client'),
        ),
    ]
