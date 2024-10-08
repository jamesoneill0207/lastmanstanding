# Generated by Django 2.2.28 on 2024-09-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_player_week_lost'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastManStanding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
