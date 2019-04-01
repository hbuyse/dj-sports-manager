# Generated by Django 2.1.7 on 2019-03-26 14:39

from django.db import migrations, models
import sports_manager.player.models
import sports_manager.player.validators
import sports_manager.storage


class Migration(migrations.Migration):

    dependencies = [
        ('sports_manager', '0014_auto_20190325_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalcertificate',
            name='renewals',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='number of renewals'),
        ),
        migrations.AlterField(
            model_name='medicalcertificate',
            name='file',
            field=models.FileField(blank=True, storage=sports_manager.storage.OverwriteStorage(), upload_to=sports_manager.player.models.medical_certificate_upload_to, validators=[sports_manager.player.validators.validate_file_extension, sports_manager.player.validators.validate_file_size], verbose_name='file'),
        ),
    ]
