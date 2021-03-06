#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Standard library
from datetime import date

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Current django project
from sports_manager.models import License, Player, Team


class TestLicenseModel(TestCase):
    """Test the License model."""

    def test_string_representation(self):
        """Test string representation."""
        owner = get_user_model().objects.create(username="toto")
        p = Player(first_name="Toto", last_name="Tata", owner=owner, birthday=date(1970,1,1))
        p.save()
        l = License(player=p, number="123456", is_payed=True)
        l.save()
        self.assertEqual(str(l), "Toto Tata (123456)")

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(License._meta.verbose_name), "license")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(License._meta.verbose_name_plural), "licenses")
