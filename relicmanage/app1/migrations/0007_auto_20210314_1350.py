# Generated by Django 3.1.2 on 2021-03-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20210314_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='photo'),
        ),
    ]