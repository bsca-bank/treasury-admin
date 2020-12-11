# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-22 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0001_initial'),
        ('treasury', '0004_fx_ctrl_cf'),
    ]

    operations = [
        migrations.AddField(
            model_name='fx',
            name='client',
            field=models.ForeignKey(blank=True, help_text='Tapez le code client ici', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tiers.ClientCtrl'),
        ),
    ]
