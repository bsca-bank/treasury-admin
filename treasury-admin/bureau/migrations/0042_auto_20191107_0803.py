# Generated by Django 2.2.6 on 2019-11-07 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0041_auto_20191107_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='nature',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bureau.MeetingType'),
            preserve_default=False,
        ),
    ]
