# Generated by Django 2.1.5 on 2019-06-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0026_auto_20190403_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalfilestorage',
            name='ref_id',
            field=models.CharField(blank=True, help_text='Référence id interne', max_length=15, null=True, verbose_name='Réf.ID'),
        ),
    ]
