# -*- coding: utf-8 -*-
"""Gymnasium implementation."""

# Django
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _  # noqa


class Gymnasium(models.Model):
    """Gymnasium model for the website."""

    GYMNASIUM_TYPE = 0
    STADIUM_TYPE = 1

    GYMNASIUM_TYPES = (
        (GYMNASIUM_TYPE, _("gymnasium")),
        (STADIUM_TYPE , _("stadium"))
    )

    slug = models.SlugField(_('slug'), unique=True, max_length=128)
    type = models.PositiveSmallIntegerField(_('type'), blank=False, choices=GYMNASIUM_TYPES, default=GYMNASIUM_TYPE)
    name = models.CharField(_('name'), max_length=128)
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    zip_code = models.IntegerField(_('zip code'))
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
    area = models.SmallIntegerField(_('area'), blank=True, null=True)
    capacity = models.SmallIntegerField(_('capacity'), blank=True, null=True)

    def __str__(self):
        """Representation of a Gymnasium as a string."""
        return "{} {}".format(self.get_type_display().title(), self.name)

    class Meta:
        verbose_name = _("gymnasium")
        verbose_name_plural = _("gymnasiums")
        ordering = ("name", "zip_code")

    def save(self, *args, **kwargs):
        """Override the save method in order to rewrite the slug field each time we save the object."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Override the get_absolute_url method in order to use it in templates."""
        return reverse("sports-manager:gymnasium-detail", kwargs={"slug": self.slug})

    def get_time_slots(self):
        """Return a list of all the time slots in the gymnasium."""
        return self.time_slot_set.all()
