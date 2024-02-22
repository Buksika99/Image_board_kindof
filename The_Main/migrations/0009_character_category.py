# Generated by Django 5.0.1 on 2024-02-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Main', '0008_remove_character_default_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='category',
            field=models.CharField(choices=[('anime', 'Anime'), ('game', 'Game')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
