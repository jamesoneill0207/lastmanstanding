# Generated by Django 2.2.28 on 2024-09-30 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_auto_20240930_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='hidden',
        ),
    ]
