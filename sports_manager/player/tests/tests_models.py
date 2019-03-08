#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

from datetime import date, timedelta

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

# Current django project
from sports_manager.player.models import file_upload_to, is_player_old_enough, Player
from sports_manager.team.models import Team
from sports_manager.tests.helper import create_user

class TestIsPlayerOldEnough(TestCase):
    """Test is_player_old_enough fn."""

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_not_old_enough(self):
        """Test the exception."""
        for i in range(0, settings.SPORTS_MANAGER_PLAYER_MIN_AGE):
            birthday = date.today() - timedelta(weeks=i*52)
            with self.assertRaises(ValidationError):
                is_player_old_enough(birthday)

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_old_enough(self):
        """Test the exception."""
        for i in range(7, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)

    @override_settings()
    def test_no_min_age_given(self):
        """Test the exception."""
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        for i in range(0, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)



class TestPlayerModel(TestCase):
    """Test the Player model."""

    def test_string_representation(self):
        """Test string representation."""
        l = Player(first_name="Toto", last_name="Tata")
        self.assertEqual(str(l), "Toto Tata")

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(Player._meta.verbose_name), "player")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(Player._meta.verbose_name_plural), "players")

    def test_save(self):
        user = create_user()[1]
        l = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user)
        self.assertEqual(len(l.slug), 0)
        l.save()
        self.assertEqual(l.slug, "toto-tata")
