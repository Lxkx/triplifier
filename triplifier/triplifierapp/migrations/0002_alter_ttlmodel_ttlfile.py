# Generated by Django 3.2.9 on 2021-11-11 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triplifierapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttlmodel',
            name='ttlFile',
            field=models.FileField(upload_to=''),
        ),
    ]
