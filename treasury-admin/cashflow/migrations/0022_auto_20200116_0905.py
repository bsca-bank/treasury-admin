# Generated by Django 2.2.6 on 2020-01-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0021_auto_20190826_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflowdetail',
            name='ref_swift',
            field=models.CharField(blank=True, help_text='Référence Swift/Sygma', max_length=50, null=True, verbose_name='Réf. Payment'),
        ),
    ]
