# Generated by Django 2.1.5 on 2019-08-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0064_auto_20190814_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='trfdossierctrl',
            name='ref_swift',
            field=models.CharField(blank=True, help_text='Référence swift du TRF/RPT', max_length=50, null=True, verbose_name='Réf. Swift'),
        ),
    ]
