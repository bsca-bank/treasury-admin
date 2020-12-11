# Generated by Django 2.2.6 on 2019-11-12 11:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bureau', '0067_auto_20191108_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetinguser',
            name='direction',
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='alias',
            field=models.CharField(blank=True, help_text='Short name', max_length=150, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='date_birth',
            field=models.DateField(default=django.utils.timezone.now, help_text='date de naissance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='date_exp_passport',
            field=models.DateField(default=django.utils.timezone.now, help_text='Date Exp. du Passport'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Femme'), (1, 'Homme')], default=1),
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, verbose_name='nationality'),
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='no_passport',
            field=models.CharField(blank=True, help_text='Numéro du Passport', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='meetinguser',
            name='position',
            field=models.CharField(blank=True, help_text='Poste', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='meetinguser',
            name='first_name',
            field=models.CharField(blank=True, help_text='Prénom', max_length=30, verbose_name='given name'),
        ),
        migrations.AlterField(
            model_name='meetinguser',
            name='last_name',
            field=models.CharField(blank=True, help_text='Nom', max_length=150, verbose_name='surname'),
        ),
    ]
