# Generated by Django 2.2.6 on 2020-02-04 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0109_auto_20200121_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trfdossierctrl',
            old_name='chk_fx',
            new_name='chk_fund',
        ),
    ]
