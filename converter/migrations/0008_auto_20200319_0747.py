# Generated by Django 3.0.4 on 2020-03-19 05:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0007_auto_20200318_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='latest_rate_update',
        ),
        migrations.AddField(
            model_name='currency',
            name='date_valid',
            field=models.DateField(default=datetime.date(2020, 3, 19)),
        ),
    ]
