# Generated by Django 3.1.2 on 2021-03-24 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_auto_20210324_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='relic_name',
            field=models.CharField(max_length=128),
        ),
    ]