# Generated by Django 2.1.5 on 2019-03-31 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0039_auto_20190331_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rptdossierexec',
            options={'verbose_name': 'RPT BO Manager', 'verbose_name_plural': 'RPT BO Manager'},
        ),
        migrations.AlterModelOptions(
            name='trfdossierexec',
            options={'managed': True, 'verbose_name': 'TRF BO Manager', 'verbose_name_plural': 'TRF BO Manager'},
        ),
    ]
