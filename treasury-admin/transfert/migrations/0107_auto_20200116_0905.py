# Generated by Django 2.2.6 on 2020-01-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0106_auto_20200114_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domdossiermulti',
            name='obs',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
