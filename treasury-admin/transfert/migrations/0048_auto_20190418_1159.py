# Generated by Django 2.1.5 on 2019-04-18 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0047_auto_20190418_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trfdossierctrl',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='util.CatalogTypeProduct'),
        ),
    ]
