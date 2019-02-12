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
from django.utils.translation import gettext_lazy as _

# Current django project
from sports_manager.storage import OverwriteStorage

logger = logging.getLogger(__name__)


def file_upload_to(instance, filename):
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
    if isinstance(instance, MedicalCertificate):
        path = os.path.join('licenses',
                            instance.owner.get_username().lower(),
                            "{team}_{fn}_{ln}".format(team=instance.team.slug.lower(),
                                                      fn=instance.first_name.lower(),
                                                      ln=instance.last_name.lower(),
                                                      ),
                            '{}_medical_certificate'.format(ext))

    logger.info("Image {filename} saved in {path}".format(path=path, filename=filename))

    return path

MIN_AGE = 6

def is_player_old_enough(birthday):
    if birthday < (date.today() - timedelta(weeks=MIN_AGE*52)):
        raise ValidationError(_("Player is not old enough (min: %(min)s years old, birthday given: %(birthday)s"),
                              params={'min': MIN_AGE, "birthday": birthday}
        )

class Player(models.Model):
    """Player model
    """

    SEXES = (
        ('MA', _('Male')),
        ('FE', _('Female'))
    )

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=150)
    sex = models.CharField(_("sex"), max_length=2, choices=SEXES)
    birthday = models.DateField(_("birthday"), validators=[is_player_old_enough])
    created = models.DateTimeField(_('creation date'), auto_now_add=True)

    def __str__(self):
        """String representation."""
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        """Meta class."""

        verbose_name = _("player")
        ordering = ("last_name", "first_name")


class MedicalCertificate(models.Model):
    """Medical certificate file model
    """

    CERTIFICATION_NOT_UPLOADED = 0
    CERTIFICATION_IN_VALIDATION = 1
    CERTIFICATION_VALID = 2
    CERTIFICATION_REJECTED = 3

    CERTIFICATION_STEPS = (
        (CERTIFICATION_NOT_UPLOADED, _("Certification not uploaded")),
        (CERTIFICATION_IN_VALIDATION, _("Certification in validation")),
        (CERTIFICATION_VALID, _("Certification valid")),
        (CERTIFICATION_REJECTED, _("Certification rejected")),
    )

    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    file = models.FileField(_('file'), upload_to=file_upload_to, null=True)
    validation = models.PositiveSmallIntegerField(_("validation"),
                                                  choices=CERTIFICATION_STEPS,
                                                  default=CERTIFICATION_NOT_UPLOADED)
    start = models.DateField(_('starting date'), auto_now_add=True)
    end = models.DateField(_('ending date'), null=True)

    class Meta:
        """Meta class."""

        verbose_name = _("medical certificate")
        ordering = ("player", "start", "validation")
    
    def is_valid(self):
        """Check if the medical certificate is valid."""
        return self.validation == self.CERTIFICATION_VALID
