# Generated by Django 2.1.5 on 2019-03-18 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0021_auto_20180325_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossiercouvr',
            name='account_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_dossiercouvr_account_couvr', to='tiers.AccountCorresp'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='account_out',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_dossiercouvr_account_pay', to='tiers.AccountCorresp'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='ccy_in',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_dossiercouvr_ccy_couvr', to='util.Ccy'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='ccy_out',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_dossiercouvr_ccy_pay', to='util.Ccy'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='corresp_in',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_dossiercouvr_corresp_couvr', to='tiers.Corresp'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='corresp_out',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_dossiercouvr_corresp_pay', to='tiers.Corresp'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='msg_commission',
            field=models.ForeignKey(blank=True, limit_choices_to={'codtype': '/CODTYPTR/018'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='msg_commission', to='settlement.SygmaCtrl'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='msg_payment',
            field=models.ForeignKey(blank=True, limit_choices_to={'codtype': '/CODTYPTR/004'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_dossiercouvr_msg_payment', to='settlement.SygmaCtrl'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='statut',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 24}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Statut'),
        ),
        migrations.AlterField(
            model_name='dossiercouvr',
            name='type_product',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 24}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Catalog_Type_Product'),
        ),
        migrations.AlterField(
            model_name='dossierctrl',
            name='oper_approv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_dossierctrl_oper_approv', to=settings.AUTH_USER_MODEL, verbose_name='Approbateur'),
        ),
        migrations.AlterField(
            model_name='dossierctrl',
            name='oper_verify',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_dossierctrl_oper_verify', to=settings.AUTH_USER_MODEL, verbose_name='Contôleur'),
        ),
        migrations.AlterField(
            model_name='dossierctrl',
            name='statut',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 26}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Statut'),
        ),
        migrations.AlterField(
            model_name='trfdossierapurectrl',
            name='dossierCtrl',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transfert_trfdossierapurectrl_dossier', to='transfert.DossierCtrl'),
        ),
        migrations.AlterField(
            model_name='trfdossierapurectrl',
            name='oper_decl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_oper_decl', to=settings.AUTH_USER_MODEL, verbose_name='Oper Decl'),
        ),
        migrations.AlterField(
            model_name='trfdossierapurectrl',
            name='oper_examen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_oper_examen', to=settings.AUTH_USER_MODEL, verbose_name='Oper Exam'),
        ),
        migrations.AlterField(
            model_name='trfdossierapurectrl',
            name='oper_recall',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierapurectrl_oper_recall', to=settings.AUTH_USER_MODEL, verbose_name='Oper Rappel'),
        ),
        migrations.AlterField(
            model_name='trfdossiercouvrctrl',
            name='statut',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 26}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Statut'),
        ),
        migrations.AlterField(
            model_name='trfdossierincomplet',
            name='oper_appro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierincomplet_oper_appro', to=settings.AUTH_USER_MODEL, verbose_name='Approuvé par'),
        ),
        migrations.AlterField(
            model_name='trfdossierincomplet',
            name='oper_ok',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierincomplet_oper_ok', to=settings.AUTH_USER_MODEL, verbose_name='Validé par'),
        ),
        migrations.AlterField(
            model_name='virementctrl',
            name='oper_approv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_virementctrl_oper_approv', to=settings.AUTH_USER_MODEL, verbose_name='Approbateur'),
        ),
        migrations.AlterField(
            model_name='virementctrl',
            name='statut',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 26}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Statut'),
        ),
        migrations.AlterField(
            model_name='virementctrl',
            name='type_product',
            field=models.ForeignKey(blank=True, limit_choices_to={'contentType': 88}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.Catalog_Type_Product'),
        ),
    ]
