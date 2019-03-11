"""."""

# Standard library
import logging
import os

# Third-party
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# Current django project
from sports_manager.storage import OverwriteStorage

logger = logging.getLogger(__name__)


def image_upload_to(instance, filename):
    """Create the path where to store the files."""
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
            ("GOL", _('gold')),
            ("SIL", _('silver')),
            ("BRO", _('bronze')),
        )),
        ('FSGT 4x4', (
            ("HAR", _('hard')),
            ("MED", _('medium')),
            ("EAS", _('easy')),
        )),
        ('FFVB', (
            # Female
            ("N1", _('elite')),
            ("N2", _('national 2')),
            ("R1", _('regional 1')),
            ("R2", _('regional 2')),
            ("R3", _('regional 3')),
            ("DEP", _('departemental')),
            ("U20", _('under 20')),
            ("U17", _('under 17')),
            ("U15", _('under 15')),
            ("U13", _('under 13')),
        ))
    )
    SEXES = (
        ('MA', _('male')),
        ('MI', _('mixed')),
        ('FE', _('female'))
    )
    slug = models.SlugField(_("slug"), unique=True, max_length=128, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='category', blank=False)
    name = models.CharField(_("name"), unique=True, max_length=128)
    level = models.CharField(_("level"), max_length=4, choices=LEVELS, blank=False)
    sex = models.CharField(_("sex"), max_length=2, choices=SEXES, blank=False)
    trainer = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                verbose_name=_('trainer'))
    url = models.URLField(_("competition URL"))
    description = MarkdownxField(_('description'))
    img = models.ImageField(_('image'), storage=OverwriteStorage(), upload_to=image_upload_to, blank=True)
    recruitment = models.BooleanField(_('is recruiting'))

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return "{} {}".format(self.name.title(), self.get_sex_display()).title()

    class Meta:
        """Meta class."""

        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ("sex", "level", "name")

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:team-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Override the save method in order to rewrite the slug field each time we save the object."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def description_md(self):
        """Get the description as HTML (not Mdown)."""
        return markdownify(self.description)

    def get_training_days(self):
        """Get the list of training days ordered by day."""
        return self.training_set.all()

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
        (MONDAY, _('monday')),
        (TUESDAY, _('tuesday')),
        (WEDNESDAY, _('wednesday')),
        (THURSDAY, _('thursday')),
        (FRIDAY, _('friday')),
        (SATURDAY, _('saturday')),
        (SUNDAY, _('sunday')),
    )
    TYPE_PRACTICE = (
        (PRACTICE, _('practice')),
        (MATCH, _('match')),
    )

    type = models.PositiveSmallIntegerField(_("type"), choices=TYPE_PRACTICE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name=_('team'))
    gymnasium = models.ForeignKey('Gymnasium', on_delete=models.CASCADE, verbose_name=_('gymnasium'))
    day = models.PositiveSmallIntegerField(_("day"), choices=DAYS_OF_WEEK)
    start = models.TimeField(_("starting time"))
    end = models.TimeField(_("ending time"))

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return "{} - {}".format(self.team.name, self.get_day_display())

    class Meta:
        """Meta class."""

        verbose_name = _("time slot")
        verbose_name_plural = _("time slots")
        ordering = ("day", "start", "end")

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:team-time-slot-detail",
                       kwargs={"team": self.object.team.slug, "pk": self.team.pk}
                       )
