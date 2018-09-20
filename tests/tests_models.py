#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dj-sports-manager` models module."""

from dj_sports_manager.models import Category, License, Team

from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCategoryModel(TestCase):
    """Test the Category model."""

    def test_string_representation(self):
        """Test string representation."""
        d = {
            "name": "Fédération Française de Volley-Ball"
        }
        c = Category(**d)
        self.assertEqual(str(c), "Fédération Française de Volley-Ball")

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(Category._meta.verbose_name), "category")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(Category._meta.verbose_name_plural), "categories")

    def test_description_md(self):
        """Test the description_md function of post class."""
        c = Category.objects.create(min_age=18)
        self.assertEqual(len(c.description_md()), 0)

        tests = (
            ("# Toto", "<h1>", "</h1>"),
            ("## Toto", "<h2>", "</h2>"),
            ("Toto", "<p>", "</p>"),
            ("*Toto*", "<em>", "</em>"),
            ("**Toto**", "<strong>", "</strong>"),
        )

        for test in tests:
            c = Category.objects.create(min_age=18, description=test[0])
            self.assertIn(test[1], c.description_md())
            self.assertIn(test[2], c.description_md())

    def test_has_teams_with_trainer(self):
        """Test the description_md function of post class."""
        c = Category.objects.create(min_age=18)
        self.assertFalse(c.has_teams_with_trainer())

        # Create team with no trainer
        Team.objects.create(category=c, is_recruiting=True)
        self.assertEqual(c.team_set.count(), 1)
        self.assertFalse(c.has_teams_with_trainer())

        # Create team with trainer
        u = get_user_model().objects.create(first_name="Toto", last_name="Toto")
        Team.objects.create(category=c, is_recruiting=False, trainer=u)
        self.assertEqual(c.team_set.count(), 2)
        self.assertTrue(c.has_teams_with_trainer())


class TestTeamModel(TestCase):
    """Test the Team model."""

    def test_string_representation(self):
        """Test string representation."""
        for s in Team.SEXES:
            t = Team(name="Dep 1", sex=s[0])
            self.assertEqual(str(t), "Dep 1 - {}".format(s[1]))

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(Team._meta.verbose_name), "team")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(Team._meta.verbose_name_plural), "teams")

    def test_description_md(self):
        """Test the description_md function of post class."""
        t = Team(name="Dep 1", sex="MI")
        self.assertEqual(len(t.description_md()), 0)

        tests = (
            ("# Toto", "<h1>", "</h1>"),
            ("## Toto", "<h2>", "</h2>"),
            ("Toto", "<p>", "</p>"),
            ("*Toto*", "<em>", "</em>"),
            ("**Toto**", "<strong>", "</strong>"),
        )

        for test in tests:
            t = Team(name="Dep 1", sex="MI", description=test[0])
            self.assertIn(test[1], t.description_md())
            self.assertIn(test[2], t.description_md())


class TestLicenseModel(TestCase):
    """Test the License model."""

    def test_string_representation(self):
        """Test string representation."""
        t = Team(name="Dep 1")
        l = License(team=t, first_name="Toto", last_name="Tata", license_number="123456")
        self.assertEqual(str(l), "Dep 1 - Toto Tata (123456)")

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(License._meta.verbose_name), "license")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(License._meta.verbose_name_plural), "licenses")
