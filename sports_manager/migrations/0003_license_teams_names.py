# Generated by Django 2.1.7 on 2019-04-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports_manager', '0002_auto_20190411_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='teams_names',
            field=models.CharField(blank=True, max_length=512, verbose_name='team names'),
        ),
    ]