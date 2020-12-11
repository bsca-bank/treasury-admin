# Generated by Django 2.2.6 on 2020-02-13 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0113_auto_20200213_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='trfdossierctrl',
            name='type_dcc',
            field=models.IntegerField(blank=True, choices=[(0, '\\REJET'), (1, '\\ACK')], help_text="Avis de DCC sur l'EXAMEN LAB-FT", null=True, verbose_name='Type DCC'),
        ),
    ]
