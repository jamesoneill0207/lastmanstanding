# Generated by Django 2.2.28 on 2024-10-03 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_team_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameweek',
            name='all_results',
            field=models.BooleanField(default=False),
        ),
    ]
