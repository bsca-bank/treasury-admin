# Generated by Django 2.1.5 on 2019-09-04 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settlement', '0015_auto_20190812_1158'),
        ('transfert', '0078_auto_20190903_1828'),
    ]

    operations = [
		migrations.RenameField(
            model_name='trfdossierctrl',
            old_name='pay_msg',
            new_name='msg_payment',
        ),
    ]
