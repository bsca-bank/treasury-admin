# Generated by Django 2.2.6 on 2020-01-22 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0044_fi_folio'),
    ]

    operations = [
        migrations.AddField(
            model_name='fi',
            name='unit',
            field=models.DecimalField(decimal_places=0, default=1000000, help_text='Nominal par unité', max_digits=18),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fi',
            name='daycount',
            field=models.IntegerField(choices=[(0, 'ACT/360'), (1, 'ACT/ACT')], default=0),
        ),
    ]
