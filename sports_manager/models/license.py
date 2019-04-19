"""."""

# Standard library
import json
import logging

# Django
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from sports_manager.models.player import Player
from sports_manager.models.team import Team

logger = logging.getLogger(__name__)


class License(models.Model):
    """License model."""

    teams = models.ManyToManyField(Team, blank=True, verbose_name=_("teams"))
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name=_("player"), blank=False)
    number = models.CharField(_("number"), max_length=20, blank=True)
    is_payed = models.BooleanField(_('has been payed'))
    created = models.DateTimeField(_('creation date'), auto_now_add=True)
    modified = models.DateTimeField(_('last modification date'), auto_now=True)
    teams_names = models.CharField(_("team names"), max_length=512, blank=True, editable=False)

    def __str__(self):
        """Representation as a string."""
        return "{} - {}".format(self.player, self.season)

    class Meta:

        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ("-created", "player")

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:license-detail",
                       kwargs={'username': self.player.owner.get_username(), 'pk': self.pk}
                       )

    @property
    def season(self):
        """Get the season based on the license's created field."""
        if self.created.date().month <= 7:
            season = "{} / {}".format(self.created.date().year - 1, self.created.date().year)
        else:
            season = "{} / {}".format(self.created.date().year, self.created.date().year + 1)
        return season

    def set_team_names(self):
        logger.debug(self.teams.all())
        self.teams_names = json.dumps([team.name for team in self.teams.all()])

    def get_team_names(self):
        return json.loads(self.teams_names)

    def save(self, *args, **kwargs):
        self.set_team_names()
        logger.debug(self.get_team_names())
        super().save(*args, **kwargs)

