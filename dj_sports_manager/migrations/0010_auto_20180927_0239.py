# Generated by Django 2.0.7 on 2018-09-27 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_sports_manager', '0009_auto_20180921_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=128, null=True, unique=True, verbose_name='category slug'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='team name'),
        ),
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(max_length=128, null=True, unique=True, verbose_name='team slug'),
        ),
    ]
