# Generated by Django 2.2.28 on 2024-09-30 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0007_remove_team_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
