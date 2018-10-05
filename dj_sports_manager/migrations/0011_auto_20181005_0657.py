# Generated by Django 2.0.7 on 2018-10-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_sports_manager', '0010_auto_20180927_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='level',
            field=models.CharField(choices=[('FSGT 6x6', (('GOL', 'Gold'), ('SIL', 'Silver'), ('BRO', 'Bronze'))), ('FSGT 4x4', (('HAR', 'Hard'), ('MED', 'Medium'), ('EAS', 'Easy'))), ('FFVB', (('N1', 'Elite'), ('N2', 'National 2'), ('R1', 'Regional 1'), ('R2', 'Regional 2'), ('R3', 'Regional 3'), ('DEP', 'Departemental')))], max_length=4, verbose_name='team level'),
        ),
    ]
