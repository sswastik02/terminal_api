# Generated by Django 3.1.7 on 2021-03-13 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='command_response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField(blank=True, default='')),
                ('response', models.TextField(blank=True, default='')),
            ],
        ),
    ]
