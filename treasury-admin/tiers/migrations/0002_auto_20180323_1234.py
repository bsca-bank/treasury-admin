# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-23 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0020_auto_20180323_1234'),
        ('treasury', '0006_auto_20180323_1234'),
        ('interface', '0008_auto_20180322_0830'),
        ('tiers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TiersCtrl',
            fields=[
                ('apbkcli_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='interface.ApBkcli')),
                ('alias', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sigle')),
                ('address', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Ctrl Tiers',
                'db_table': 'THIRD_TIERS',
                'managed': True,
                'verbose_name_plural': 'Ctrl Client',
            },
            bases=('interface.apbkcli',),
        ),
        migrations.RemoveField(
            model_name='accountcpty',
            name='ccy',
        ),
        migrations.RemoveField(
            model_name='accountcpty',
            name='cpty',
        ),
        migrations.RemoveField(
            model_name='accountdepository',
            name='depository',
        ),
        migrations.DeleteModel(
            name='Autorite',
        ),
        migrations.DeleteModel(
            name='Broker',
        ),
        migrations.DeleteModel(
            name='Emetteur',
        ),
        migrations.DeleteModel(
            name='Market',
        ),
        migrations.RemoveField(
            model_name='accountcorresp',
            name='id_ap',
        ),
        migrations.RemoveField(
            model_name='corresp',
            name='address',
        ),
        migrations.RemoveField(
            model_name='corresp',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='corresp',
            name='id_ap',
        ),
        migrations.AddField(
            model_name='accountcorresp',
            name='fullname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientctrl',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
