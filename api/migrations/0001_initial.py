# Generated by Django 3.0.7 on 2020-07-25 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('currency', models.CharField(max_length=25, unique=True)),
                ('frequency', models.IntegerField()),
            ],
        ),
    ]
