# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-25 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0016_auto_20180325_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fxclifile',
            name='dossier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treasury.FXCli'),
        ),
        migrations.AlterModelTable(
            name='fxcli',
            table='TRESOR_FX_CLI',
        ),
        migrations.AlterModelTable(
            name='fxclifile',
            table='TRESOR_FX_CLI_FILE',
        ),
    ]
