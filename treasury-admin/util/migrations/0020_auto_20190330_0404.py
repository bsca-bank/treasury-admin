# Generated by Django 2.1.2 on 2019-03-29 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0023_auto_20190318_1626'),
        ('treasury', '0028_auto_20190318_1627'),
        ('transfert', '0022_auto_20190318_1627'),
        ('cashflow', '0015_auto_20190318_1616'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('bureau', '0009_auto_20181010_2252'),
        ('util', '0019_auto_20190330_0352'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catalog_Type_Act',
            new_name='CatalogTypeActivity',
        ),
        migrations.RenameModel(
            old_name='Catalog_Type_Doc',
            new_name='CatalogTypeFile',
        ),
        migrations.RenameModel(
            old_name='Catalog_Type_Product',
            new_name='CatalogTypeProduct',
        ),
        migrations.RenameModel(
            old_name='Catalog_Type_Tiers',
            new_name='CatalogTypeTiers',
        ),
        migrations.AlterModelOptions(
            name='catalogtypecommercial',
            options={'managed': True, 'ordering': ('level', 'nature'), 'verbose_name': 'Contrôle de nomenclature commercial', 'verbose_name_plural': 'Contrôle de nomenclature commercial'},
        ),
        migrations.AlterModelOptions(
            name='ccy',
            options={'managed': True, 'ordering': ('iso',)},
        ),
        migrations.RenameField(
            model_name='catalogtypefile',
            old_name='contentType',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='catalogtypeproduct',
            old_name='contentType',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='catalogtypetiers',
            old_name='contentType',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='statut',
            old_name='contentType',
            new_name='content_type',
        ),
        migrations.AddField(
            model_name='catalogtypecommercial',
            name='chk_dom',
            field=models.BooleanField(default=True, help_text='Check here if a dom document needed', verbose_name='Dom'),
        ),
        migrations.AddField(
            model_name='catalogtypecommercial',
            name='code_nature',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='C_Nature'),
        ),
        migrations.AddField(
            model_name='catalogtypecommercial',
            name='code_oper',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='C_Oper'),
        ),
        migrations.AddField(
            model_name='catalogtypecommercial',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catalogtypecommercial',
            name='parent_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.CatalogTypeCommercial'),
        ),
    ]
