#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dj-sports-manager` models module."""

from dj_sports_manager.models import Category

from django.test import TestCase


class TestCategoryModel(TestCase):

    def test_string_representation(self):
        d = {
            "name": "Fédération Française de Volley-Ball"
        }
        s = Category(**d)
        self.assertEqual(str(s), "Fédération Française de Volley-Ball")

    def test_verbose_name(self):
        self.assertEqual(str(Category._meta.verbose_name), "category")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "categories")

    def test_description_md(self):
        """Test the description_md function of post class."""
        s = Category.objects.create(min_age=18)
        self.assertEqual(len(s.description_md()), 0)

        s = Category.objects.create(min_age=18, description="# Toto")
        self.assertIn("<h1>", s.description_md())
        self.assertIn("</h1>", s.description_md())

        s = Category.objects.create(min_age=18, description="## Toto")
        self.assertIn("<h2>", s.description_md())
        self.assertIn("</h2>", s.description_md())

        s = Category.objects.create(min_age=18, description="Toto")
        self.assertIn("<p>", s.description_md())
        self.assertIn("</p>", s.description_md())

        s = Category.objects.create(min_age=18, description="*Toto*")
        self.assertIn("<em>", s.description_md())
        self.assertIn("</em>", s.description_md())

        s = Category.objects.create(min_age=18, description="**Toto**")
        self.assertIn("<strong>", s.description_md())
        self.assertIn("</strong>", s.description_md())

    def test_has_teams_with_trainer(self):
        """Test the description_md function of post class."""
        s = Category.objects.create(min_age=18)
        self.assertFalse(s.has_teams_with_trainer())
