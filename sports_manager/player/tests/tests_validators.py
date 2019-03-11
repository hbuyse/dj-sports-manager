#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Standard library
from datetime import date, timedelta

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

# Current django project
from sports_manager.player.validators import is_player_old_enough


class TestIsPlayerOldEnough(TestCase):

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_not_old_enough(self):
        for i in range(0, settings.SPORTS_MANAGER_PLAYER_MIN_AGE):
            birthday = date.today() - timedelta(weeks=i*52)
            with self.assertRaises(ValidationError):
                is_player_old_enough(birthday)

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_old_enough(self):
        for i in range(7, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)

    @override_settings()
    def test_no_min_age_given(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        for i in range(0, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)