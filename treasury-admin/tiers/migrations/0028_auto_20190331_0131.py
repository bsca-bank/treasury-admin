# Generated by Django 2.1.2 on 2019-03-30 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0027_auto_20190331_0033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientfilestorage',
            old_name='fileName',
            new_name='file_name',
        ),
    ]
