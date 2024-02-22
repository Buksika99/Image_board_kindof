# Generated by Django 5.0.1 on 2024-02-22 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Main', '0009_character_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='character',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
