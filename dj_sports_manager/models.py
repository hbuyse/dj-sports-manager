"""."""

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Category(models.Model):
    """Sport category model."""

    name = models.CharField(_('category name'), max_length=128)
    img = models.CharField(_('category image name'), max_length=128)
    min_age = models.PositiveSmallIntegerField(_('category minimal age'))
    max_age = models.PositiveSmallIntegerField(_('category maximal age'), blank=True, null=True)
    summary = models.CharField(_('category summary'), max_length=512)
    description = MarkdownxField(_('category description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("name",)

    @property
    def formatted_description(self):
        return markdownify(self.description)

    def has_team_with_trainer(self):
        return True if Team.objects.filter(category=self, trainer__isnull=False) else False


class Team(models.Model):
    LEVELS = (
        ('FSGT 6x6', (
            ("OR", _('Gold')),
            ("ARG", _('Silver')),
            ("BRO", _('Bronze')),
        )
        ),
        ('FSGT 4x4', (
            ("HAR", _('Hard')),
            ("MED", _('Medium')),
            ("EAS", _('Easy')),
        )
        ),
        ('FFVB', (
            ("N1", _('Elite')),
            ("N2", _('National 2')),
            ("R1", _('Regional 1')),
            ("R2", _('Regional 2')),
            ("R3", _('Regional 3')),
            ("DEP", _('Departemental')),
        )
        ),
        ('Pleasure', (
            ("PLE", _("Pleasure")),
        )
        )
    )
    SEXES = (
        ('MA', _('Male')),
        ('MI', _('Mixed')),
        ('FE', _('Female'))
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(_("Team name"), max_length=128)
    level = models.CharField(_("Level"), max_length=3, choices=LEVELS)
    sex = models.CharField(_("Sexe"), max_length=2, choices=SEXES)
    trainer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(_("Competition URL"))
    description = MarkdownxField(_('team description'), blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.get_sex_display())

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ("sex", "level", "name")

    @property
    def formatted_description(self):
        return markdownify(self.description)

    def get_training_days(self):
        return self.training_set.order_by("day")

    def get_players(self):
        return self.licence_set.order_by("last_name")


class Practice(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    PRACTICE = 0
    MATCH = 1

    DAYS_OF_WEEK = (
        (MONDAY, _('Monday')),
        (TUESDAY, _('Tuesday')),
        (WEDNESDAY, _('Wednesday')),
        (THURSDAY, _('Thursday')),
        (FRIDAY, _('Friday')),
        (SATURDAY, _('Saturday')),
        (SUNDAY, _('Sunday')),
    )
    TYPE_PRACTICE = (
        (PRACTICE, _('Practice')),
        (MATCH, _('Match')),
    )

    type_practice = models.PositiveSmallIntegerField(_("Practice type"), choices=TYPE_PRACTICE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(_("Practice day"), choices=DAYS_OF_WEEK)
    start = models.TimeField(_("Practice starting time"))
    end = models.TimeField(_("Practice starting time"))
    gymnasium = models.ForeignKey('dj_gymnasiums.Gymnasium', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.team.name, self.get_day_display())

    class Meta:
        verbose_name = _("practice")
        verbose_name_plural = _("practices")
        ordering = ("day",)


class License(models.Model):
    SEXES = (
        ('MA', _('Male')),
        ('FE', _('Female'))
    )
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(_("license person first name"), max_length=30)
    last_name = models.CharField(_("license person last name"), max_length=150)
    sex = models.CharField(_("sex"), max_length=2, choices=SEXES)
    birthday = models.DateField(_("birthday"))
    license_number = models.CharField(_("license number"), max_length=20, blank=True)

    def __str__(self):
        return "{} - {} {} ({})".format(self.team.name, self.first_name, self.last_name, self.license_number)

    class Meta:
        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ("team", "first_name", "last_name")
