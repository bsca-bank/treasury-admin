# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 09:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apbkcom',
            name='ctrl',
        ),
    ]
