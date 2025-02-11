# Generated by Django 2.2.6 on 2020-02-04 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transfert', '0110_auto_20200204_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='trfdossierctrl',
            name='oper_fund',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierctrl_oper_fund', to=settings.AUTH_USER_MODEL, verbose_name='Agent de Validation du Fond'),
        ),
        migrations.AlterField(
            model_name='trfdossierctrl',
            name='chk_fund',
            field=models.BooleanField(default=False, help_text='Cochez en après la selection du type fund', verbose_name='Chk Fund_Type'),
        ),
    ]
