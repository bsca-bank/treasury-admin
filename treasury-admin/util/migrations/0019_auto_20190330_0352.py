# Generated by Django 2.1.2 on 2019-03-29 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0022_auto_20190318_1627'),
        ('util', '0018_auto_20190318_1616'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catalog_Type_Commercial',
            new_name='CatalogTypeCommercial',
        ),
    ]
