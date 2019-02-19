#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Current django project
from sports_manager.models import Category, Team
from sports_manager.models.category import image_upload_to


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

    def test_save_override(self):
        """Test save override."""
        d = {
            "name": "Fédération Française de Volley-Ball",
            'min_age': 7
        }
        c = Category.objects.create(**d)
        self.assertEqual(c.slug, "federation-francaise-de-volley-ball")

    def test_get_absolute_url(self):
        """Test the description_md function of post class."""
        d = {
            'name': "Fédération Française de Volley-Ball",
            'min_age': 7
        }
        c = Category.objects.create(**d)
        self.assertEqual(c.get_absolute_url(), "/category/federation-francaise-de-volley-ball/")

    def test_description_md(self):
        """Test the description_md function of post class."""
        i = 0
        c = Category.objects.create(name=str(i), min_age=18)
        self.assertEqual(len(c.description_md()), 0)

        tests = (
            ("# Toto", "<h1>", "</h1>"),
            ("## Toto", "<h2>", "</h2>"),
            ("Toto", "<p>", "</p>"),
            ("*Toto*", "<em>", "</em>"),
            ("**Toto**", "<strong>", "</strong>"),
        )

        for test in tests:
            i += 1
            c = Category.objects.create(name=str(i), min_age=18, description=test[0])
            self.assertIn(test[1], c.description_md())
            self.assertIn(test[2], c.description_md())

    def test_has_teams_with_trainer(self):
        """Test the description_md function of post class."""
        c = Category.objects.create(min_age=18)
        self.assertFalse(c.has_teams_with_trainer())

        # Create team with no trainer
        Team.objects.create(category=c, name='a', recrutment=True)
        self.assertEqual(c.team_set.count(), 1)
        self.assertFalse(c.has_teams_with_trainer())

        # Create team with trainer
        u = get_user_model().objects.create(first_name="Toto", last_name="Toto")
        Team.objects.create(category=c, name='b', recrutment=False, trainer=u)
        self.assertEqual(c.team_set.count(), 2)
        self.assertTrue(c.has_teams_with_trainer())

    def test_path_image_upload_to(self):
        """Test image_upload_to function for Category."""
        c = Category.objects.create(min_age=18)
        self.assertEqual(image_upload_to(c, "toto.png"), 'categories/img.png')

        c = Category.objects.create(name="Hello-World", min_age=18)
        self.assertEqual(image_upload_to(c, "toto.png"), 'categories/hello-world/img.png')
