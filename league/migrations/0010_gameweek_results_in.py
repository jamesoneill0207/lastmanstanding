# Generated by Django 2.2.28 on 2024-10-03 23:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0009_gameweek_all_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameweek',
            name='results_in',
            field=models.DateTimeField(default=datetime.datetime(2025, 10, 1, 15, 30)),
        ),
    ]
