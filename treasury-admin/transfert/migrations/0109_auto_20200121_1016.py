# Generated by Django 2.2.6 on 2020-01-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0108_auto_20200116_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domdossiermulti',
            name='obs',
            field=models.TextField(blank=True, default="Nous n'avons pas reçu votre dossier d'apurement.", max_length=1000, null=True),
        ),
    ]
