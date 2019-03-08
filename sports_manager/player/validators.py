# -*- coding: utf-8 -*-
"""Validator functions."""

# Standard library
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
    try:
        if birthday > (date.today() - timedelta(weeks=(settings.SPORTS_MANAGER_PLAYER_MIN_AGE * 52))):
            raise ValidationError(_("Player is not old enough (min: %(min)s years old, birthday given: %(birthday)s)"),
                                  params={'min': settings.SPORTS_MANAGER_PLAYER_MIN_AGE, "birthday": birthday}
                                  )
    except AttributeError:
        pass
