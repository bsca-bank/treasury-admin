# Generated by Django 2.1.5 on 2019-08-26 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('util', '0037_auto_20190826_0814'),
        ('transfert', '0066_auto_20190826_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrfDossierApureCtrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chk_verify', models.BooleanField(default=False, help_text='1st Agent', verbose_name='Verify')),
                ('time_verify', models.DateTimeField(blank=True, editable=False, help_text='Time Verify', null=True)),
                ('chk_approv', models.BooleanField(default=False, help_text='2nd Agent', verbose_name='Approv')),
                ('time_approv', models.DateTimeField(blank=True, editable=False, help_text='Time Approv', null=True)),
                ('obs', models.TextField(blank=True, max_length=1000, null=True)),
                ('docTraceLog', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_docTraceLog', to='util.DocTraceLog')),
                ('dossier_dom', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_dossierDom', to='transfert.DomDossierCtrl', verbose_name='Dossier de Domiciliation')),
                ('oper_approv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_approv', to=settings.AUTH_USER_MODEL)),
                ('oper_input', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_oper_input', to=settings.AUTH_USER_MODEL, verbose_name='Agent')),
                ('oper_verify', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_verify', to=settings.AUTH_USER_MODEL)),
                ('statut', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_statut', to='util.Statut')),
            ],
            options={
                'db_table': 'trf_dossier_apure_ctrl',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TrfDossierApureDetail',
            fields=[
                ('trfdossierctrl_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transfert.TrfDossierCtrl')),
                ('trfDossierApureCtrl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_trfdossierapuredetail_trfDossierApureCtrl', to='transfert.TrfDossierApureCtrl', verbose_name='Ticket Parent')),
            ],
            options={
                'db_table': 'trf_dossier_apure',
                'managed': True,
            },
            bases=('transfert.trfdossierctrl',),
        ),
        migrations.RemoveField(
            model_name='trfdossiercouvr',
            name='releveCmpt',
        ),
        migrations.AddField(
            model_name='trfdossiercouvr',
            name='ref_swift',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Réf. Swift'),
        ),
        migrations.AddField(
            model_name='domdossierctrl',
            name='trfDossierApureCtrl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_domdossierctrl_statut', to='transfert.TrfDossierApureCtrl', verbose_name="Contrôle d'Apurement"),
        ),
    ]
