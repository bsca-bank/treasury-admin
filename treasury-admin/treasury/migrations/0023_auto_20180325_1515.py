# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-25 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0021_auto_20180324_1403'),
        ('treasury', '0022_auto_20180325_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fxclifile',
            name='dossier',
        ),
        migrations.RemoveField(
            model_name='fxcli',
            name='fxCliFile',
        ),
        migrations.AddField(
            model_name='fxcli',
            name='cliFile',
            field=models.ForeignKey(blank=True, help_text='Client Confirmation', null=True, on_delete=django.db.models.deletion.CASCADE, to='tiers.ClientCtrlFile', verbose_name='Document'),
        ),
        migrations.DeleteModel(
            name='FXCliFile',
        ),
    ]
