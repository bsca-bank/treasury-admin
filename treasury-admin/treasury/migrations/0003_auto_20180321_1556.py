# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-21 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0002_auto_20171016_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tresorlimit',
            name='montant_act',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Le Solde Actuel', max_digits=18, null=True, verbose_name='Montant Actuel (Estim\xe9)'),
        ),
        migrations.AlterField(
            model_name='tresorlimit',
            name='montant_max',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Le Solde Maximum', max_digits=18, null=True, verbose_name='Max Balance'),
        ),
        migrations.AlterField(
            model_name='tresorlimit',
            name='montant_min',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Le Solde Minimum', max_digits=18, null=True, verbose_name='Min Balance'),
        ),
        migrations.AlterField(
            model_name='tresorlimit',
            name='montant_val',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Le Solde du dernier relv\xe9 de compte', max_digits=18, null=True, verbose_name='Balance du correspondant'),
        ),
    ]
