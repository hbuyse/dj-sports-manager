# Generated by Django 2.0.7 on 2019-03-22 14:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sports_manager', '0012_auto_20190321_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalcertificate',
            name='start',
            field=models.DateField(verbose_name='starting date'),
        ),
        migrations.AlterField(
            model_name='team',
            name='sex',
            field=models.CharField(choices=[('FE', 'female'), ('MA', 'male'), ('MI', 'mixed')], max_length=2, verbose_name='sex'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('first_name', 'last_name', 'owner')},
        ),
    ]