# Generated by Django 2.1.5 on 2019-04-18 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0024_auto_20190403_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogtypeproduct',
            name='code_product',
            field=models.CharField(default=99, max_length=10, verbose_name='Code. Product'),
            preserve_default=False,
        ),
    ]
