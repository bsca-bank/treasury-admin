# Generated by Django 2.1.5 on 2019-09-03 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0072_auto_20190827_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='docTraceLog',
        ),
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='dossier_dom',
        ),
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='oper_approv',
        ),
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='oper_input',
        ),
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='oper_verify',
        ),
        migrations.RemoveField(
            model_name='trfdossierapurectrl',
            name='statut',
        ),
        migrations.RemoveField(
            model_name='trfdossierapuredetail',
            name='trfDossierApureCtrl',
        ),
        migrations.RemoveField(
            model_name='trfdossierapuredetail',
            name='trfdossierctrl_ptr',
        ),
        migrations.RemoveField(
            model_name='domdossierctrl',
            name='trfDossierApureCtrl',
        ),
        migrations.DeleteModel(
            name='TrfDossierApureCtrl',
        ),
        migrations.DeleteModel(
            name='TrfDossierApureDetail',
        ),
    ]
