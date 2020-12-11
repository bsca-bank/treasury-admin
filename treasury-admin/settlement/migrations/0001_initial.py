# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-08 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tiers.corresp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SygmaCtrl',
            fields=[
                ('sygma_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='interface.Sygma')),
                ('ctrl', models.BooleanField(db_column='CTRL', default=False)),
            ],
            options={
                'verbose_name': 'Contr\xf4le de SYGMA',
                'db_table': 'TRESOR_SYGMA_CTRL',
                'managed': True,
                'verbose_name_plural': 'Contr\xf4le de SYGMA',
            },
            bases=('interface.sygma',),
        ),
        migrations.CreateModel(
            name='TreasuryPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.IntegerField(choices=[(0, 'Agence'), (1, 'Correspondant')], default=0)),
                ('date_val', models.DateField(verbose_name='DATE_VAL')),
                ('montant_op', models.DecimalField(blank=True, decimal_places=2, default=0, help_text="La solde d'ouverture", max_digits=18, null=True, verbose_name='Opening Balance')),
                ('montant', models.DecimalField(decimal_places=2, default=0, help_text='La solde de la cl\xf4ture', max_digits=18, verbose_name='Closing Balance')),
                ('bs_file', models.FileField(blank=True, help_text='T\xe9l\xe9charger le relev\xe9 de compte scann\xe9 en PDF', null=True, upload_to=tiers.corresp.models.upload_path_handler, verbose_name='R\xe9lev\xe9 de compte')),
            ],
            options={
                'managed': True,
                'ordering': ('-date_val',),
                'verbose_name_plural': 'Contr\xf4le de la solde de tr\xe9sorerie',
                'db_table': 'TRESOR_LORO_CORRESP',
                'verbose_name': 'Contr\xf4le de la solde de tr\xe9sorerie',
            },
        ),
    ]
