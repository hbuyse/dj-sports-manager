#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Standard library
from datetime import date, datetime
from unittest import mock

# Third-party
import pytz

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

# Current django project
from sports_manager.models.license import License
from sports_manager.models.player import Player
from sports_manager.models.team import Team


class TestLicenseModel(TestCase):
    """Test the License model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = get_user_model().objects.create(username="toto")
        cls.player = Player.objects.create(first_name="Toto", last_name="Tata",
                                           owner=cls.owner, birthday=date(1970, 1, 1))

    def test_string_representation(self):
        """Test string representation."""
        l = License(player=self.player, number="123456", is_payed=True)
        l.save()
        self.assertIn("Toto Tata", str(l))
        self.assertIn(str(date.today().year), str(l))

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(License._meta.verbose_name), "license")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(License._meta.verbose_name_plural), "licenses")

    def test_get_absolute_url(self):
        l = License(player=self.player, number="123456", is_payed=True)
        l.save()
        self.assertEqual(l.get_absolute_url(), "/toto/license/{}/".format(l.pk))

    def test_season_property(self):
        for year in [2015, 2016, 2017, 2018]:
            with mock.patch('django.utils.timezone.now') as mock_now:
                # make "now" following the year
                mock_now.return_value = datetime(year, 7, 31, tzinfo=pytz.UTC)
                l = License(player=self.player, number="123456", is_payed=True)
                l.save()
                self.assertEqual(l.season, "{} / {}".format(year - 1, year))

            with mock.patch('django.utils.timezone.now') as mock_now:
                # make "now" following the year
                mock_now.return_value = datetime(year, 8, 1, tzinfo=pytz.UTC)
                l = License(player=self.player, number="123456", is_payed=True)
                l.save()
                self.assertEqual(l.season, "{} / {}".format(year, year + 1))
