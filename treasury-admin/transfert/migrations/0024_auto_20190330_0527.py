# Generated by Django 2.1.2 on 2019-03-29 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0023_delete_dossiercouvrcashflow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DossierCtrlProxyFO',
        ),
        migrations.DeleteModel(
            name='TrfDossierIncompletProxyFO',
        ),
    ]
