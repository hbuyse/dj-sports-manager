# -*- coding: utf-8 -*-
"""Validator functions."""

# Standard library
import os
from datetime import date, timedelta

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def is_player_old_enough(birthday):
    """Check if the player that will be created as the minimal age required.

    This validator check for the SPORTS_MANAGER_PLAYER_MIN_AGE variable in settings.py.
    If the variable is not present, then we suppose that there is no minimal age so the age is not verified.
    """
    if hasattr(settings, 'SPORTS_MANAGER_PLAYER_MIN_AGE'):
        if birthday > (date.today() - timedelta(weeks=(settings.SPORTS_MANAGER_PLAYER_MIN_AGE * 52))):
            raise ValidationError(_("Player is not old enough (min: %(min)s years old, birthday given: %(birthday)s)"),
                                  params={'min': settings.SPORTS_MANAGER_PLAYER_MIN_AGE, "birthday": birthday}
                                  )


def validate_file_extension(value):
    """Validate the extension of the uploaded file."""
    if hasattr(settings, 'SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST'):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        if not ext.lower() in settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST:
            raise ValidationError(_('Unsupported file extension. Valid extension: %(ext_list)s'),
                                  params={'ext_list': ', '.join(settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST)}
                                  )


def validate_file_size(value):
    """Validate that the file's size is lower than 2MB."""
    if hasattr(settings, 'SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB'):
        max_size = settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB << 20
        if value.size > max_size:
            raise ValidationError(_("The maximum file size that can be uploaded is %(size)d MB"),
                                  params={'size': settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB}
                                  )
