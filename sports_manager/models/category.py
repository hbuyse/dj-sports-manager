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
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Current django project
from sports_manager.models.team import Team
from sports_manager.storage import OverwriteStorage

logger = logging.getLogger(__name__)


def image_upload_to(instance, filename):
    """Create the path where to store the files.

    If the file instance is a Sponsor, the file has to be the logo so it will be uploaded to
        MEDIA_ROOT/sponsors/<sponsor_name>/logo<ext>.
    """
    path = None
    basename, ext = os.path.splitext(filename)
    if isinstance(instance, Category):
        path = os.path.join('categories', instance.slug, 'img{}'.format(ext))

    logger.info("Image {filename} saved in {path}".format(path=path, filename=filename))

    return path


class Category(models.Model):
    """Sport category model."""

    slug = models.SlugField(_("slug"), unique=True, max_length=128, null=True)
    name = models.CharField(_('name'), unique=True, max_length=128)
    img = models.ImageField(_('image'), storage=OverwriteStorage(), upload_to=image_upload_to, blank=True)
    min_age = models.PositiveSmallIntegerField(_('minimal age'))
    max_age = models.PositiveSmallIntegerField(_('maximal age'), blank=True, null=True)
    summary = models.TextField(_('summary'), max_length=512)
    description = MarkdownxField(_('description'))

    def __str__(self):
        """String representation."""
        return self.name

    class Meta:
        """Meta class."""

        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("name",)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def description_md(self):
        """Return the text mardownified."""
        return markdownify(self.description)

    def has_teams_with_trainer(self):
        """Check if there is at least a team in this category that have a trainer."""
        return True if Team.objects.filter(category=self, trainer__isnull=False) else False
