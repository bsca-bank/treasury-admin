# Generated by Django 2.2.6 on 2019-11-07 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0051_remove_meetingitem_date_val'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='obs',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
