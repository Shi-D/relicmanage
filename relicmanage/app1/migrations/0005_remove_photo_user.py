# Generated by Django 3.1.2 on 2021-03-14 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_relic_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='user',
        ),
    ]