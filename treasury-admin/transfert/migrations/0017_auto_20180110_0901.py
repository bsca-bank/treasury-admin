# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-10 08:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0016_auto_20180110_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virementctrl',
            name='date_go',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='virementctrl',
            name='date_val',
            field=models.DateField(blank=True, null=True),
        ),
    ]
