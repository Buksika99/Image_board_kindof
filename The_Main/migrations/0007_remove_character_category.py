# Generated by Django 5.0.1 on 2024-02-22 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('The_Main', '0006_remove_gamecharacter_character_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='category',
        ),
    ]