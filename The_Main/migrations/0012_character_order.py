# Generated by Django 5.0.1 on 2024-02-22 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Main', '0011_alter_character_options_remove_character_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]