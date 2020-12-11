# Generated by Django 2.2.6 on 2020-01-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0042_auto_20200116_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collateral',
            name='decot_pct',
            field=models.DecimalField(decimal_places=4, help_text='Taux de Decot', max_digits=7, verbose_name='Decot'),
        ),
    ]
