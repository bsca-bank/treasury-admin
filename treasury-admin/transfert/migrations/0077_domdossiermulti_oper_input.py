# Generated by Django 2.1.5 on 2019-09-03 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transfert', '0076_auto_20190903_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='domdossiermulti',
            name='oper_input',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_domdossiermulti_oper_input', to=settings.AUTH_USER_MODEL, verbose_name='Agent'),
        ),
    ]
