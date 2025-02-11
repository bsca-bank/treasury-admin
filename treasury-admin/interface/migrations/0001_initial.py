# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-08 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApBkcli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(max_length=50, unique=True)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('chk_actif', models.BooleanField(default=False, help_text='Cochez si la client normal', verbose_name='Chk Actif')),
                ('date_profil', models.DateField(blank=True, null=True, verbose_name='Date de Cr\xe9ation')),
                ('date_val', models.DateField(blank=True, null=True, verbose_name='Date de Modification')),
            ],
            options={
                'ordering': ('ref_id',),
                'verbose_name': 'Interface Amplitude client (BKCLI)',
                'db_table': 'AP_BKCLI',
                'managed': True,
                'verbose_name_plural': 'Interface Amplitude client (BKCLI)',
            },
        ),
        migrations.CreateModel(
            name='ApBkcom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.CharField(blank=True, db_column='AGE', max_length=5, null=True)),
                ('date_val', models.DateField(db_column='DATE_VAL')),
                ('date_cr', models.DateField(blank=True, db_column='DATE_CR', null=True)),
                ('date_dr', models.DateField(blank=True, db_column='DATE_DR', null=True)),
                ('code_client', models.CharField(blank=True, db_column='CLI', max_length=6, null=True)),
                ('acc', models.CharField(db_column='ACC', max_length=6)),
                ('acc_txt', models.CharField(blank=True, db_column='ACC_TXT', max_length=100, null=True)),
                ('ccy_code', models.CharField(db_column='CCY_CODE', max_length=3)),
                ('montant', models.DecimalField(db_column='AMT', decimal_places=2, max_digits=18)),
                ('ctrl', models.BooleanField(db_column='CTRL', default=False)),
                ('timestamp', models.CharField(db_column='TIMESTAMP', max_length=12)),
            ],
            options={
                'verbose_name': 'Interface Amplitude A/C Balance (BKCOM)',
                'db_table': 'AP_BKCOM',
                'managed': True,
                'verbose_name_plural': 'Interface Amplitude A/C Balance (BKCOM)',
            },
        ),
        migrations.CreateModel(
            name='ApBkdopi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.CharField(db_column='NATURE', max_length=3)),
                ('agenceID', models.CharField(blank=True, db_column='AGENCE_ID', max_length=5, null=True)),
                ('ref_id', models.CharField(db_column='REF_ID', max_length=11)),
                ('statut_sys', models.CharField(db_column='STATUT_SYS', max_length=2)),
                ('ccy_code', models.CharField(db_column='CCY_CODE', max_length=3)),
                ('operType', models.CharField(blank=True, db_column='OTRF', max_length=1, null=True)),
                ('donneur', models.CharField(blank=True, db_column='DONNEUR', max_length=200, null=True)),
                ('accDonneur', models.CharField(blank=True, db_column='NCPDO', max_length=11, null=True)),
                ('benef', models.CharField(blank=True, db_column='BENEF', max_length=200, null=True)),
                ('accBenef', models.CharField(blank=True, db_column='NCPBF', max_length=11, null=True)),
                ('montant', models.DecimalField(db_column='MONTANT', decimal_places=2, max_digits=18)),
                ('montant_xaf', models.DecimalField(db_column='MONTANT_XAF', decimal_places=0, max_digits=18)),
                ('fxRate', models.DecimalField(blank=True, db_column='FX_RATE', decimal_places=7, max_digits=12, null=True)),
                ('date_val', models.CharField(db_column='DATE_VAL', max_length=8)),
                ('date_exec', models.CharField(blank=True, db_column='DATE_EXEC', max_length=8, null=True)),
                ('invoice', models.CharField(blank=True, db_column='INV', max_length=200, null=True)),
                ('feeType', models.CharField(blank=True, db_column='FEE_TYPE', max_length=3, null=True)),
                ('motif', models.TextField(blank=True, db_column='MOTIF', null=True)),
                ('uti', models.CharField(blank=True, db_column='UTI', max_length=5, null=True)),
                ('timestamp', models.CharField(db_column='TIMESTAMP', max_length=12)),
            ],
            options={
                'db_table': 'AP_BKDOPI',
                'verbose_name': 'Interface Amplitude TRF/RPT (BKDOPI)',
                'verbose_name_plural': 'Interface Amplitude TRF/RPT (BKDOPI)',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ApBkmvt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(db_column='ETA', max_length=2)),
                ('entity', models.CharField(blank=True, db_column='AGE', max_length=5, null=True)),
                ('date_val', models.DateField(db_column='DVA')),
                ('date_trd', models.DateField(blank=True, db_column='DSAI', null=True)),
                ('time_trd', models.TimeField(blank=True, db_column='HSAI', null=True)),
                ('code_client', models.CharField(db_column='CLI', max_length=6)),
                ('alias', models.CharField(db_column='NOMP', max_length=200)),
                ('acc', models.CharField(db_column='NCP', max_length=11)),
                ('nature', models.CharField(db_column='NAT', max_length=6)),
                ('direction', models.CharField(db_column='SEN', max_length=1)),
                ('ccy_code1', models.CharField(blank=True, db_column='DEVC', max_length=3, null=True)),
                ('montant1', models.DecimalField(db_column='MHTT', decimal_places=2, max_digits=18)),
                ('ccy_code2', models.CharField(blank=True, db_column='DEVA', max_length=3, null=True)),
                ('montant2', models.DecimalField(db_column='MNAT', decimal_places=2, max_digits=18)),
                ('fx_rate', models.DecimalField(db_column='TCAI2', decimal_places=8, max_digits=18)),
                ('ctrl', models.BooleanField(db_column='CTRL', default=False)),
                ('timestamp', models.CharField(db_column='TIMESTAMP', max_length=12)),
            ],
            options={
                'verbose_name': 'Interface Amplitude Fx Retail (BKMVT)',
                'db_table': 'AP_BKMVT',
                'managed': True,
                'verbose_name_plural': 'Interface Amplitude Fx Retail (BKMVT)',
            },
        ),
        migrations.CreateModel(
            name='Sygma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cf', models.IntegerField(choices=[(0, 'N/A'), (1, 'CF_InFlow'), (2, 'CF_OutFlow')], default=0)),
                ('date_val', models.DateField()),
                ('ref_id', models.CharField(max_length=50)),
                ('type_msg', models.CharField(max_length=3)),
                ('statut_msg', models.CharField(blank=True, max_length=5, null=True)),
                ('codtype', models.CharField(blank=True, max_length=13, null=True)),
                ('ccy', models.CharField(blank=True, max_length=3, null=True)),
                ('montant', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('expd', models.CharField(max_length=12)),
                ('dest', models.CharField(max_length=12)),
                ('info', models.TextField(blank=True, max_length=255, null=True)),
                ('link_id', models.CharField(blank=True, max_length=12, null=True)),
                ('donneur', models.CharField(blank=True, max_length=50, null=True)),
                ('benef', models.CharField(blank=True, max_length=50, null=True)),
                ('cmpt_expd', models.CharField(blank=True, max_length=12, null=True)),
                ('corr_expd', models.CharField(blank=True, max_length=12, null=True)),
                ('cmpt_dest', models.CharField(blank=True, max_length=12, null=True)),
                ('corr_dest', models.CharField(blank=True, max_length=12, null=True)),
                ('charge_type', models.CharField(blank=True, max_length=3, null=True)),
                ('obs', models.TextField(blank=True, null=True)),
                ('timestamp', models.CharField(blank=True, db_column='timestamp', max_length=12, null=True)),
            ],
            options={
                'verbose_name': 'Interface SYGMA',
                'db_table': 'SYGMA',
                'managed': True,
                'verbose_name_plural': 'Interface SYGMA',
            },
        ),
        migrations.AlterUniqueTogether(
            name='apbkdopi',
            unique_together=set([('ref_id', 'statut_sys')]),
        ),
    ]
