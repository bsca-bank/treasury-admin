# Generated by Django 2.2.6 on 2019-11-07 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0048_auto_20191107_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingdoc',
            name='meeting_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bureau.MeetingUser'),
        ),
    ]
