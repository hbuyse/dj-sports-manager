#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Current django project
from sports_manager.category.models import Category
from sports_manager.team.models import Team, image_upload_to
from sports_manager.tests.helper import CategoryHelper, TeamHelper


class TestImageUploadTo(TestCase):
    """Test the path creation function."""

    def test_with_no_team_object(self):
        obj = 0
        self.assertEqual(image_upload_to(obj, 'Toto.img'), None)

    def test_with_team_object(self):
        obj = Team(slug='hello-world')
        self.assertEqual(image_upload_to(obj, 'Toto.img'), 'teams/hello-world/team.img')


class TestTeamModel(TestCase):
    """Test the Team model."""

    def setUp(self):
        self.helper = TeamHelper(name='Régional 1')

    def test_string_representation(self):
        """Test string representation."""
        obj = self.helper.object
        self.assertEqual(str(self.helper.object), "Régional 1 Mixed")

    def test_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(str(Team._meta.verbose_name), "team")

    def test_verbose_name_plural(self):
        """Test the plural verbose name."""
        self.assertEqual(str(Team._meta.verbose_name_plural), "teams")

    def test_save_override(self):
        """Test save override."""
        self.assertEqual(self.helper.get('slug'), "regional-1")

    def test_get_absolute_url(self):
        """Test the description_md function of the class."""
        self.assertEqual(self.helper.object.get_absolute_url(), "/team/regional-1/")

    def test_description_md(self):
        """Test the description_md property of the class."""
        tests = (
            (),
            ("# Toto", "<h1>", "</h1>"),
            ("## Toto", "<h2>", "</h2>"),
            ("Toto", "<p>", "</p>"),
            ("*Toto*", "<em>", "</em>"),
            ("**Toto**", "<strong>", "</strong>"),
        )

        for test in tests:
            i = tests.index(test)
            if i == 0:
                obj = Team(name=str(i), category=self.helper.get('category'), recruitment=False)
                obj.save()
                self.assertEqual(len(obj.description_md), 0)
            else:
                obj = Team(name=str(i), description=test[0], category=self.helper.get('category'), recruitment=False)
                obj.save()
                self.assertIn(test[1], obj.description_md)
                self.assertIn(test[2], obj.description_md)
