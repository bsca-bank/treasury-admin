# Generated by Django 2.2.6 on 2020-11-09 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0050_fi_coupon_couru'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fi',
            name='coupon_couru',
            field=models.DecimalField(decimal_places=2, help_text="Coupon couru à l'acquisition", max_digits=18),
        ),
    ]
