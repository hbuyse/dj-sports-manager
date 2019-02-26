"""."""

# Standard library
from datetime import date
import logging
import os

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Current django project
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

logger = logging.getLogger(__name__)


class License(models.Model):
    """License model."""

    teams = models.ManyToManyField('Team', blank=True, verbose_name=_("teams"))
    player = models.ForeignKey('Player', on_delete=models.CASCADE, verbose_name=_("player"), blank=False)
    number = models.CharField(_("number"), max_length=20, blank=True)
    is_payed = models.BooleanField(_('has been payed'))
    created = models.DateTimeField(_('creation date'), auto_now_add=True)
    modified = models.DateTimeField(_('last modification date'), auto_now=True)

    def __str__(self):
        """String representation."""
        return "{} ({})".format(self.player, self.number)

    class Meta:
        """Meta class."""

        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ("-created", "player")
    
    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:license-detail",
                       kwargs={'username': self.player.owner.get_username(), 'pk': self.pk}
        )

    def get_season(self):
        """Get the season based on the license's created field."""
        current_year = date.today().year
        if self.created.date() < date(current_year, 7, 15):
            season = "{} / {}".format(current_year-1, current_year)
        else:
            season = "{} / {}".format(current_year, current_year + 1)
        return season