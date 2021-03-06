# Generated by Django 3.2.5 on 2021-07-16 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0003_team_teamemployee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamemployee',
            name='update_date',
        ),
        migrations.AddField(
            model_name='team',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Last updated'),
        ),
    ]
