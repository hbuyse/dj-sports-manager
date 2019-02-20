"""."""

# Standard library
import logging
import os
from datetime import date, timedelta

# Django
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Current django project
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from sports_manager.storage import OverwriteStorage

logger = logging.getLogger(__name__)


def file_upload_to(instance, filename):
    """Callback to create the path where to store the files.
    
    result: 
    """
    basename, ext = os.path.splitext(filename)
    if isinstance(instance, MedicalCertificate):
        path = os.path.join(instance.player.owner.get_username().lower(),
                            "{fn}_{ln}".format(fn=instance.player.first_name.lower(),
                                               ln=instance.player.last_name.lower(),
                            ),
                            str(date.today().year),
                            'medical_certificate{ext}'.format(ext=ext))
        logger.info("Medical certificate {filename} saved in {path}".format(path=path, filename=filename))

    return path

MIN_AGE = 6

def is_player_old_enough(birthday):
    if birthday > (date.today() - timedelta(weeks=MIN_AGE*52)):
        raise ValidationError(_("Player is not old enough (min: %(min)s years old, birthday given: %(birthday)s)"),
                              params={'min': MIN_AGE, "birthday": birthday}
        )

class Player(models.Model):
    """Player model

    TODO: Link with an urgence contact.
    """

    SEXES = (
        ('MA', _('male')),
        ('FE', _('female'))
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
        verbose_name_plural = _("players")
        ordering = ("last_name", "first_name")
    
    def get_last_medical_certificate(self):
        """Retrieve the last medical certificate uploaded."""
        return self.medicalcertificate_set.last()


class MedicalCertificate(models.Model):
    """Medical certificate file model
    """

    NOT_UPLOADED = 0
    IN_VALIDATION = 1
    VALID = 2
    REJECTED = 3

    CERTIFICATION_STEPS = (
        (NOT_UPLOADED, _("not uploaded")),
        (IN_VALIDATION, _("in validation")),
        (VALID, _("valid")),
        (REJECTED, _("rejected")),
    )

    player = models.ForeignKey("Player", on_delete=models.CASCADE, verbose_name=_('player'))
    file = models.FileField(_('file'), upload_to=file_upload_to, blank=True)
    validation = models.PositiveSmallIntegerField(_("validation step"),
                                                  choices=CERTIFICATION_STEPS,
                                                  default=NOT_UPLOADED,
                                                  blank=False)
    start = models.DateField(_('starting date'), auto_now_add=True)
    end = models.DateField(_('ending date'), null=True)
    created = models.DateTimeField(_('creation date'), auto_now_add=True)

    class Meta:
        """Meta class."""

        verbose_name = _("medical certificate")
        verbose_name_plural = _("medical certificates")
        ordering = ("player", "start", "validation")
    
    def is_valid(self):
        """Check if the medical certificate is valid."""
        return self.validation == self.CERTIFICATION_VALID


class EmergencyContact(models.Model):
    """Emergency contact linked to a Player."""

    player = models.ForeignKey("Player", on_delete=models.CASCADE, verbose_name=_('player'))
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email"), max_length=255, blank=True)
    phone = models.CharField(
        _('phone number'),
        max_length=10,
        validators=[
            # ^
            #     (?:(?:\+|00)33|0)     # Dialing code
            #     \s*[1-9]              # First number (from 1 to 9)
            #     (?:[\s.-]*\d{2}){4}   # End of the phone number
            # $
            RegexValidator(regex=r"^(?:(?:\+|00)33|0)\s*[1-7,9](?:[\s.-]*\d{2}){4}$",
                           message=_("This is not a correct phone number"))
        ]
    )