# Generated by Django 2.1.5 on 2019-09-10 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0084_auto_20190910_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='trfdossierctrl',
            name='ctrl_cf',
            field=models.BooleanField(default=True, help_text='Check if genrerate cashflow', verbose_name='Genr Cashflow'),
        ),
    ]
