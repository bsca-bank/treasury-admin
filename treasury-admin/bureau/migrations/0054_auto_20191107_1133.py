# Generated by Django 2.2.6 on 2019-11-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0053_auto_20191107_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingitem',
            name='name_cn',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='meetingitem',
            name='name_fr',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
