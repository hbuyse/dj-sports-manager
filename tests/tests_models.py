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
