# Generated by Django 5.0.1 on 2024-02-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DanbooruImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('tags', models.CharField(max_length=255)),
            ],
        ),
    ]
