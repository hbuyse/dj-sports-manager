"""."""

# Standard library
import logging
import os

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Current django project
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

logger = logging.getLogger(__name__)


class License(models.Model):
    """License model.

    TODO: Link with an urgence contact.
    """
    # Team
    team = models.ManyToManyField('Team', blank=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    number = models.CharField(_("number"), max_length=20, blank=True)
    is_payed = models.BooleanField(_('has been payed'))
    created = models.DateTimeField('creation date', auto_now_add=True)
    modified = models.DateTimeField('last modification date', auto_now=True)

    def __str__(self):
        """String representation."""
        return "{} ({})".format(self.player, self.number)

    class Meta:
        """Meta class."""

        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ("player",)
