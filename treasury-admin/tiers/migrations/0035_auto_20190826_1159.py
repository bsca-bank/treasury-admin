# Generated by Django 2.1.5 on 2019-08-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0034_auto_20190812_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientctrl',
            name='niu',
            field=models.CharField(blank=True, help_text="NIU ou autre numéro d'identification de l'établissement", max_length=50, null=True, verbose_name='NIU'),
        ),
    ]
