# Generated by Django 2.2.6 on 2020-01-14 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0038_auto_20190903_1706'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('notification', '0004_auto_20191121_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailctrl',
            name='exp_no',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='emailctrl',
            name='send_no',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='emailctrl',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_emailctrl_type_product', to='util.CatalogTypeProduct'),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='emailctrl',
            name='chk_approv',
            field=models.BooleanField(default=False, help_text='2nd Agent', verbose_name='Appv'),
        ),
        migrations.AlterField(
            model_name='emailctrl',
            name='chk_verify',
            field=models.BooleanField(default=False, help_text='1st Agent', verbose_name='Verf'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='chk_approv',
            field=models.BooleanField(default=False, help_text='2nd Agent', verbose_name='Appv'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='chk_verify',
            field=models.BooleanField(default=False, help_text='1st Agent', verbose_name='Verf'),
        ),
    ]
