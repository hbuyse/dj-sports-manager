"""."""

# Standard library
import logging
import os
from datetime import date, timedelta

# Django
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# Current django project
from sports_manager.player.validators import is_player_old_enough, validate_file_extension, validate_file_size
from sports_manager.storage import OverwriteStorage

logger = logging.getLogger(__name__)


def medical_certificate_upload_to(instance, filename):
    """Create the path where to store the files.

    result: path to the file
    """
    path = None
    ext = os.path.splitext(filename)[1]
    if isinstance(instance, MedicalCertificate):
        path = os.path.join(instance.player.owner.get_username().lower(),
                            instance.player.slug,
                            str(date.today().year),
                            'medical_certificate{ext}'.format(ext=ext)
                            )
        logger.info("Medical certificate {} saved in {}".format(filename, path))

    return path


def identity_card_upload_to(instance, filename):
    """Create the path where to store the files.

    result: path to the file
    """
    path = None
    ext = os.path.splitext(filename)[1]
    if isinstance(instance, Player):
        path = os.path.join(instance.owner.get_username().lower(),
                            instance.slug,
                            'identity_card{ext}'.format(ext=ext)
                            )
        logger.info("Identity card {} saved in {}".format(filename, path))

    return path


def identity_photo_upload_to(instance, filename):
    """Create the path where to store the files.

    result: path to the file
    """
    path = None
    ext = os.path.splitext(filename)[1]
    if isinstance(instance, Player):
        path = os.path.join(instance.owner.get_username().lower(),
                            instance.slug,
                            'identity_photo{ext}'.format(ext=ext)
                            )
    logger.info("Identity photo {} saved in {}".format(filename, path))

    return path


class Player(models.Model):
    """Player model.

    TODO: Link with an urgence contact.
    """

    SEX_FEMALE = 'FE'
    SEX_MALE = 'MA'

    SEXES = (
        (SEX_FEMALE, _('female')),
        (SEX_MALE, _('male')),
    )

    slug = models.SlugField(_("slug"), max_length=128, editable=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=150)
    sex = models.CharField(_("sex"), max_length=2, choices=SEXES, blank=False)
    birthday = models.DateField(_("birthday"), validators=[is_player_old_enough])
    address = models.CharField(_("address"), max_length=256)
    add_address = models.CharField(_("additional address"), max_length=256, blank=True)
    zip_code = models.CharField(_("zip code"), max_length=5)
    city = models.CharField(_("city"), max_length=128)
    phone = models.CharField(
        _('phone number'),
        max_length=10,
        blank=True,
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
    identity_card = models.FileField(_('identity card'),
                            storage=OverwriteStorage(),
                            upload_to=identity_card_upload_to,
                            validators=[validate_file_extension, validate_file_size],
                            blank=True
                            )
    identity_photo = models.ImageField(_('identity photo'),
                            storage=OverwriteStorage(),
                            upload_to=identity_photo_upload_to,
                            validators=[validate_file_extension, validate_file_size],
                            blank=True
                            )
    email = models.EmailField(_("email"), blank=True)
    created = models.DateTimeField(_('creation date'), auto_now_add=True)

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        """Meta class."""

        verbose_name = _("player")
        verbose_name_plural = _("players")
        ordering = ("last_name", "first_name")
        unique_together = ('first_name', 'last_name', 'owner',)

    def save(self, *args, **kwargs):
        """Override the save method in order to rewrite the slug field each time we save the object."""
        self.slug = slugify("{} {}".format(self.first_name, self.last_name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:player-detail",
                       kwargs={"username": self.owner.get_username(), "slug": self.slug}
                       )

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_last_medical_certificate(self):
        """Retrieve the last medical certificate uploaded."""
        return self.medicalcertificate_set.last()


class MedicalCertificate(models.Model):
    """Medical certificate file model."""

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
    file = models.FileField(_('file'),
                            storage=OverwriteStorage(),
                            upload_to=medical_certificate_upload_to,
                            validators=[validate_file_extension, validate_file_size],
                            blank=True
                            )
    validation = models.PositiveSmallIntegerField(_("validation step"),
                                                  choices=CERTIFICATION_STEPS,
                                                  default=NOT_UPLOADED,
                                                  blank=False)
    start = models.DateField(_('starting date'))
    end = models.DateField(_('ending date'), null=True)
    renewals = models.PositiveSmallIntegerField(_("number of renewals"), default=0)
    created = models.DateTimeField(_('creation date'), auto_now_add=True)

    class Meta:
        """Meta class."""

        verbose_name = _("medical certificate")
        verbose_name_plural = _("medical certificates")
        ordering = ("player", "-start", "validation")

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return _("%(player)s (%(validation)s - start: %(start)s)") % {
            'player': self.player,
            'validation': self.get_validation_display(),
            'start': self.start
        }

    def is_valid(self):
        """Check if the medical certificate is valid."""
        return self.validation == self.VALID

    def can_be_renewed(self):
        """Check if the medical certificate can be renewed for another year."""
        return self.is_valid() and self.renewals < settings.SPORTS_MANAGER_MEDICAL_CERTIFICATE_MAX_RENEW

    def save(self, *args, **kwargs):
        """On creation, update start field.

        We do not use 'auto_now_add=True' because if we do, it will not be possible to modify it later.
        """
        if not self.pk:
            self.start = date.today()
        self.end = date(year=self.start.year + 1 + self.renewals, month=self.start.month, day=self.start.day)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:player-medical-certificate-detail",
                       kwargs={"username": self.player.owner.get_username(), "player": self.player.slug, "pk": self.pk}
                       )


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

    class Meta:
        """Meta class."""

        verbose_name = _("emergency contact")
        verbose_name_plural = _("emergency contacts")
        ordering = ("player", "first_name", "last_name")

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return "{} {} ({})".format(self.first_name, self.last_name, self.player)

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:player-emergency-contact-detail",
                       kwargs={"username": self.player.owner.get_username(), "player": self.player.slug, "pk": self.pk}
                       )
