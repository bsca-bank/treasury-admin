# Generated by Django 2.1.5 on 2019-09-03 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0075_auto_20190903_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domdossierapureproxy',
            options={'verbose_name': 'DOM Dossier BO Mgr.', 'verbose_name_plural': 'DOM Dossier BO Mgr.'},
        ),
        migrations.AlterModelOptions(
            name='domdossierctrl',
            options={'managed': True, 'verbose_name': 'DOM Dossier Ctrl.', 'verbose_name_plural': 'DOM Dossier Ctrl.'},
        ),
    ]
