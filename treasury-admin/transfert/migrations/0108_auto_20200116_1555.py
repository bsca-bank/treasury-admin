# Generated by Django 2.2.6 on 2020-01-16 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0107_auto_20200116_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trfdossiercouvr',
            name='type_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_trfdossiercouvr_type_product', to='util.CatalogTypeProduct'),
        ),
    ]
