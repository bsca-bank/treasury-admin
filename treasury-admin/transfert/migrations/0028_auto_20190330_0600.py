# Generated by Django 2.1.2 on 2019-03-29 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settlement', '0009_auto_20190330_0426'),
        ('tiers', '0024_auto_20190330_0412'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('util', '0020_auto_20190330_0404'),
        ('transfert', '0027_auto_20190330_0555'),
    ]

    operations = [
		migrations.RenameModel(
			old_name='DossierCouvr',
			new_name='TrfDossierCouvr',
        ),
    ]
