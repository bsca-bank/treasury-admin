# Generated by Django 2.2.6 on 2019-11-07 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0055_auto_20191107_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingitem',
            name='ref_no',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
