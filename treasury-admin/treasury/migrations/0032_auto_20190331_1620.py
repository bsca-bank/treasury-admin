# Generated by Django 2.1.5 on 2019-03-31 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0031_auto_20190330_2323'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='fi',
            table='tresor_fi_mgr',
        ),
        migrations.AlterModelTable(
            name='fx',
            table='tresor_fx_mgr',
        ),
        migrations.AlterModelTable(
            name='fxcli',
            table='tresor_fx_cli',
        ),
        migrations.AlterModelTable(
            name='mm',
            table='tresor_mm_mgr',
        ),
    ]
