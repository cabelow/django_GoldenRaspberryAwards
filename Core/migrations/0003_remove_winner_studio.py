# Generated by Django 4.2 on 2024-11-30 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_movie_studio_winner_movie_studio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winner',
            name='studio',
        ),
    ]
