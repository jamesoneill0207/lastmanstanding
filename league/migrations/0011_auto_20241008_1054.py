# Generated by Django 2.2.28 on 2024-10-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0010_gameweek_results_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameweek',
            name='results_in',
            field=models.DateTimeField(),
        ),
    ]
