# Generated by Django 2.1.5 on 2019-05-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0026_doctracelog_doctracelogdetail'),
        ('transfert', '0052_auto_20190529_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='trfdossierctrl',
            name='docTraceLog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfert_trfdossierctrl_docTraceLog', to='util.DocTraceLog'),
        ),
    ]
