"""."""

# Standard library
import logging
import os

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Current django project
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from sports_manager.models.gymnasium import Gymnasium
from sports_manager.storage import OverwriteStorage

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
    if isinstance(instance, Team):
        path = os.path.join('teams', instance.slug, 'team{}'.format(ext))

    logger.info("Image {filename} saved in {path}".format(path=path, filename=filename))

    return path

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
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def description_md(self):
        """Get the description as HTML (not Mdown)."""
        return markdownify(self.description)

    def get_training_days(self):
        """Get the list of training days ordered by day."""
        return self.training_set.order_by("day")

    def get_players(self):
        """Get the list of teamates of the team."""
        return self.license_set.order_by("last_name")


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

    type = models.PositiveSmallIntegerField(_("type"), choices=TYPE_PRACTICE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    gymnasium = models.ForeignKey('Gymnasium', on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(_("day"), choices=DAYS_OF_WEEK)
    start = models.TimeField(_("starting time"))
    end = models.TimeField(_("starting time"))
    # gymnasium = models.ForeignKey('dj_gymnasiums.Gymnasium', on_delete=models.CASCADE)

    def __str__(self):
        """String representation."""
        return "{} - {}".format(self.team.name, self.get_day_display())

    class Meta:
        """Meta class."""

        verbose_name = _("time slot")
        ordering = ("day", "start", "end")
