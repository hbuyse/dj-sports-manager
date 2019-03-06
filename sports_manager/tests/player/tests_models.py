#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Current django project
from sports_manager.player.models import Player
from sports_manager.team.models import Team


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
