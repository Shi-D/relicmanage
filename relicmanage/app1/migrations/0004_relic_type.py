# Generated by Django 3.1.2 on 2021-03-14 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20201022_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='relic',
            name='type',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
