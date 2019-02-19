# Generated by Django 2.0.7 on 2019-02-19 16:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import sports_manager.models.category
import sports_manager.models.player
import sports_manager.models.team
import sports_manager.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=128, null=True, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('img', models.ImageField(blank=True, storage=sports_manager.storage.OverwriteStorage(), upload_to=sports_manager.models.category.image_upload_to, verbose_name='image')),
                ('min_age', models.PositiveSmallIntegerField(verbose_name='minimal age')),
                ('max_age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='maximal age')),
                ('summary', models.TextField(max_length=512, verbose_name='summary')),
                ('description', markdownx.models.MarkdownxField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='This is not a correct phone number', regex='^(?:(?:\\+|00)33|0)\\s*[1-7,9](?:[\\s.-]*\\d{2}){4}$')], verbose_name='phone number')),
            ],
        ),
        migrations.CreateModel(
            name='Gymnasium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('zip_code', models.IntegerField(verbose_name='zip code')),
                ('phone', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='This is not a correct phone number', regex='^(?:(?:\\+|00)33|0)\\s*[1-7,9](?:[\\s.-]*\\d{2}){4}$')], verbose_name='phone number')),
                ('surface', models.SmallIntegerField(blank=True, null=True, verbose_name='surface')),
                ('capacity', models.SmallIntegerField(blank=True, null=True, verbose_name='capacity')),
            ],
            options={
                'verbose_name': 'gymnasium',
                'verbose_name_plural': 'gymnasiums',
                'ordering': ('name', 'city'),
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, verbose_name='number')),
                ('is_payed', models.BooleanField(verbose_name='has been payed')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modification date')),
            ],
            options={
                'verbose_name': 'license',
                'verbose_name_plural': 'licenses',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='MedicalCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to=sports_manager.models.player.file_upload_to, verbose_name='file')),
                ('validation', models.PositiveSmallIntegerField(choices=[(0, 'not uploaded'), (1, 'in validation'), (2, 'valid'), (3, 'rejected')], default=0, verbose_name='validation step')),
                ('start', models.DateField(auto_now_add=True, verbose_name='starting date')),
                ('end', models.DateField(null=True, verbose_name='ending date')),
            ],
            options={
                'verbose_name': 'medical certificate',
                'verbose_name_plural': 'medical certificates',
                'ordering': ('player', 'start', 'validation'),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('sex', models.CharField(choices=[('MA', 'male'), ('FE', 'female')], max_length=2, verbose_name='sex')),
                ('birthday', models.DateField(validators=[sports_manager.models.player.is_player_old_enough], verbose_name='birthday')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'player',
                'verbose_name_plural': 'players',
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=128, null=True, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('level', models.CharField(choices=[('FSGT 6x6', (('GOL', 'gold'), ('SIL', 'silver'), ('BRO', 'bronze'))), ('FSGT 4x4', (('HAR', 'hard'), ('MED', 'medium'), ('EAS', 'easy'))), ('FFVB', (('N1', 'elite'), ('N2', 'national 2'), ('R1', 'regional 1'), ('R2', 'regional 2'), ('R3', 'regional 3'), ('DEP', 'departemental'), ('U20', 'under 20'), ('U17', 'under 17'), ('U15', 'under 15'), ('U13', 'under 13')))], max_length=4, verbose_name='level')),
                ('sex', models.CharField(choices=[('MA', 'male'), ('MI', 'mixed'), ('FE', 'female')], max_length=2, verbose_name='sex')),
                ('url', models.URLField(verbose_name='competition URL')),
                ('description', markdownx.models.MarkdownxField(verbose_name='description')),
                ('img', models.ImageField(blank=True, storage=sports_manager.storage.OverwriteStorage(), upload_to=sports_manager.models.team.image_upload_to, verbose_name='image')),
                ('recrutment', models.BooleanField(verbose_name='is recruting')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Category', verbose_name='category')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='trainer')),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
                'ordering': ('sex', 'level', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'practice'), (1, 'match')], verbose_name='type')),
                ('day', models.PositiveSmallIntegerField(choices=[(0, 'monday'), (1, 'tuesday'), (2, 'wednesday'), (3, 'thursday'), (4, 'friday'), (5, 'saturday'), (6, 'sunday')], verbose_name='day')),
                ('start', models.TimeField(verbose_name='starting time')),
                ('end', models.TimeField(verbose_name='ending time')),
                ('gymnasium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Gymnasium', verbose_name='gymnasium')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Team', verbose_name='team')),
            ],
            options={
                'verbose_name': 'time slot',
                'verbose_name_plural': 'time slots',
                'ordering': ('day', 'start', 'end'),
            },
        ),
        migrations.AddField(
            model_name='medicalcertificate',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Player', verbose_name='player'),
        ),
        migrations.AddField(
            model_name='license',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Player', verbose_name='player'),
        ),
        migrations.AddField(
            model_name='license',
            name='teams',
            field=models.ManyToManyField(blank=True, to='sports_manager.Team', verbose_name='teams'),
        ),
        migrations.AddField(
            model_name='emergencycontact',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports_manager.Player', verbose_name='player'),
        ),
    ]
