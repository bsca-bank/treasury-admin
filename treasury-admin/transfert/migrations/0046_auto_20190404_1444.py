# Generated by Django 2.1.5 on 2019-04-04 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0045_auto_20190403_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domdossierctrl',
            options={'managed': True, 'ordering': ('-id',), 'verbose_name': 'DOM Dossier Manager', 'verbose_name_plural': 'DOM Dossier Manager'},
        ),
    ]
