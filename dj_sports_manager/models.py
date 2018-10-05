"""."""

import os
import logging

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from .storage import OverwriteStorage


logger = logging.getLogger(__name__)


def image_upload_to(instance, filename):
    """Callback to create the path where to store the files.

    If the file instance is a Sponsor, the file has to be the logo so it will be uploaded to
        MEDIA_ROOT/sponsors/<sponsor_name>/logo<ext>.
    If the file instance is a SponsorImage, the file has to be an image so it will be uploaded to
        MEDIA_ROOT/sponsors/<sponsor_name>/images/<filename>.
    If the file instance is a SponsorFile, the file has to be a file so it will be uploaded to
        MEDIA_ROOT/sponsors/<sponsor_name>/files/<filename>.
    """
    path = None
    basename, ext = os.path.splitext(filename)
    if isinstance(instance, Category):
        path = os.path.join('categories', instance.slug, 'img{}'.format(ext))
    elif isinstance(instance, Team):
        path = os.path.join('teams', instance.slug, 'team{}'.format(ext))
    elif isinstance(instance, License):
        path = os.path.join('licenses',
                            instance.owner.get_username().lower(),
                            "{team}_{fn}_{ln}".format(team=instance.team.slug.lower(),
                                                      fn=instance.first_name.lower(),
                                                      ln=instance.last_name.lower(),
                                                      ),
                            'medical_certification'.format(ext))

    logger.info("Image {filename} saved in {path}".format(path=path, filename=filename))

    return path


class Category(models.Model):
    """Sport category model."""

    slug = models.SlugField(_("category slug"), unique=True, max_length=128, null=True)
    name = models.CharField(_('category name'), unique=True, max_length=128)
    img = models.ImageField(_('category img'), storage=OverwriteStorage(), upload_to=image_upload_to, blank=True)
    min_age = models.PositiveSmallIntegerField(_('category minimal age'))
    max_age = models.PositiveSmallIntegerField(_('category maximal age'), blank=True, null=True)
    summary = models.TextField(_('category summary'), max_length=512)
    description = MarkdownxField(_('category description'))

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("name",)

    def description_md(self):
        """Return the text mardownified."""
        return markdownify(self.description)

    def has_teams_with_trainer(self):
        """Check if there is at least a team in this category that have a trainer."""
        return True if Team.objects.filter(category=self, trainer__isnull=False) else False


class Team(models.Model):
    """Team model."""

    LEVELS = (
        ('FSGT 6x6', (
            ("GOL", _('Gold')),
            ("SIL", _('Silver')),
            ("BRO", _('Bronze')),
        )),
        ('FSGT 4x4', (
            ("HAR", _('Hard')),
            ("MED", _('Medium')),
            ("EAS", _('Easy')),
        )),
        ('FFVB', (
            # Female
            ("N1", _('Elite')),
            ("N2", _('National 2')),
            ("R1", _('Regional 1')),
            ("R2", _('Regional 2')),
            ("R3", _('Regional 3')),
            ("DEP", _('Departemental')),
            ("U20", _('Under 20')),
            ("U17", _('Under 17')),
            ("U15", _('Under 15')),
            ("U13", _('Under 13')),
        ))
    )
    SEXES = (
        ('MA', _('Male')),
        ('MI', _('Mixed')),
        ('FE', _('Female'))
    )
    slug = models.SlugField(_("team slug"), unique=True, max_length=128, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(_("team name"), unique=True, max_length=128)
    level = models.CharField(_("team level"), max_length=4, choices=LEVELS)
    sex = models.CharField(_("team sex"), max_length=2, choices=SEXES)
    trainer = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    url = models.URLField(_("team competition URL"))
    description = MarkdownxField(_('team description'))
    img = models.ImageField(_('team img'), storage=OverwriteStorage(), upload_to=image_upload_to, blank=True)
    is_recruiting = models.BooleanField(_('team recruitement'))

    def __str__(self):
        """String representation."""
        return "{} - {}".format(self.name, self.get_sex_display())

    class Meta:
        """Meta class."""

        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ("sex", "level", "name")

    def description_md(self):
        """Get the description as HTML (not Mdown)."""
        return markdownify(self.description)

    def get_training_days(self):
        """Get the list of training days ordered by day."""
        return self.training_set.order_by("day")

    def get_players(self):
        """Get the list of teamates of the team."""
        return self.licence_set.order_by("last_name")


class TimeSlot(models.Model):
    """Time slot model."""

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

    type_time_slot = models.PositiveSmallIntegerField(_("time slot type"), choices=TYPE_PRACTICE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(_("time slot day"), choices=DAYS_OF_WEEK)
    start = models.TimeField(_("time slot starting time"))
    end = models.TimeField(_("time slot starting time"))
    gymnasium = models.ForeignKey('dj_gymnasiums.Gymnasium', on_delete=models.CASCADE)

    def __str__(self):
        """String representation."""
        return "{} - {}".format(self.team.name, self.get_day_display())

    class Meta:
        """Meta class."""

        verbose_name = _("practice")
        verbose_name_plural = _("practices")
        ordering = ("day",)


class License(models.Model):
    """Licence model.

    TODO: Link with an urgence contact.
    """

    CERTIFICATION_NOT_UPLOADED = 0
    CERTIFICATION_IN_VALIDATION = 1
    CERTIFICATION_VALID = 2
    CERTIFICATION_REJECTED = 3

    SEXES = (
        ('MA', _('Male')),
        ('FE', _('Female'))
    )

    CERTIFICATION_STEPS = (
        (CERTIFICATION_NOT_UPLOADED, _("Certification not uploaded")),
        (CERTIFICATION_IN_VALIDATION, _("Certification in validation")),
        (CERTIFICATION_VALID, _("Certification valid")),
        (CERTIFICATION_REJECTED, _("Certification rejected")),
    )
    # Team
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(_("licensee first name"), max_length=30)
    last_name = models.CharField(_("licensee last name"), max_length=150)
    sex = models.CharField(_("sex"), max_length=2, choices=SEXES)
    birthday = models.DateField(_("birthday"))
    license_number = models.CharField(_("license number"), max_length=20, blank=True)
    # Possibility to add a medical certification after having created the license
    certif = models.FileField(_('license medical certification'), upload_to=image_upload_to, blank=True)
    certif_valid = models.PositiveSmallIntegerField(_("license medical certification validation"),
                                                    choices=CERTIFICATION_STEPS,
                                                    default=CERTIFICATION_NOT_UPLOADED)
    is_payed = models.BooleanField(_('licence payed'))
    is_captain = models.BooleanField(_("is team captain"), default=False)
    created = models.DateTimeField('licence creation date', auto_now_add=True)
    modified = models.DateTimeField('licence last modification date', auto_now=True)

    def __str__(self):
        """String representation."""
        if self.license_number:
            s = "License n°" + self.license_number
        else:
            s = "{} {} - {}".format(self.first_name, self.last_name, self.team.name)
        return s

    class Meta:
        """Meta class."""

        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ("team", "first_name", "last_name")
