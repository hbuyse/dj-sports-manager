"""."""

# Standard library
import logging

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class Season(models.Model):
    """Season model."""

    slug = models.SlugField(_("slug"), unique=True, max_length=128, null=True, editable=False)
    start = models.DateField(_("starting date"), unique=True)
    end = models.DateField(_("ending date"), unique=True)
    created = models.DateTimeField(_('creation date'), auto_now_add=True)
    modified = models.DateTimeField(_('modification date'), auto_now=True)

    def __str__(self):
        """Representation of a Season as a string."""
        if self.start.year == self.end.year:
            return "{}".format(self.start.year)
        else:
            return "{} / {}".format(self.start.year, self.end.year)

    class Meta:
        """Meta class."""

        verbose_name = _("season")
        verbose_name_plural = _("seasons")
        ordering = ("start", "end")

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:season-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Override the save method in order to rewrite the slug field each time we save the object."""
        self.slug = slugify("{}-{}".format(self.start.year, self.end.year))
        super().save(*args, **kwargs)
