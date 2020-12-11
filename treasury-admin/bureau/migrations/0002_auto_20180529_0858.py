# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-29 07:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internaldoc',
            name='agentChk',
        ),
        migrations.RemoveField(
            model_name='internaldoc',
            name='demandeur',
        ),
        migrations.RemoveField(
            model_name='internaldoc',
            name='nature',
        ),
        migrations.RemoveField(
            model_name='internaldoc',
            name='statut',
        ),
        migrations.RemoveField(
            model_name='internaldocfile',
            name='agent1',
        ),
        migrations.RemoveField(
            model_name='internaldocfile',
            name='agent2',
        ),
        migrations.RemoveField(
            model_name='internaldocfile',
            name='dossier',
        ),
        migrations.DeleteModel(
            name='InternalDoc',
        ),
        migrations.DeleteModel(
            name='InternalDocFile',
        ),
        migrations.DeleteModel(
            name='InternalDocNature',
        ),
    ]
