#!/usr/bin/env python
# coding=utf-8

"""Tests for `gymnasiums` models module."""

# Django
from django.test import TestCase

# Current django project
from sports_manager.gymnasium.models import Gymnasium


class TestGymnasiumModel(TestCase):
    """Test post class model."""

    def setUp(self):
        """Setup function."""
        self.dict = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'area': '123',
            'capacity': '456',
        }

    def test_string_representation(self):
        """Test the string representation of the post model."""
        g = Gymnasium(**self.dict)
        self.assertEqual(str(g), "Gymnasium {}".format(g.name))

    def test_verbose_name(self):
        """Test the verbose name in singular."""
        self.assertEqual(str(Gymnasium._meta.verbose_name), "gymnasium")

    def test_verbose_name_plural(self):
        """Test the verbose name in plural."""
        self.assertEqual(str(Gymnasium._meta.verbose_name_plural), "gymnasiums")

    def test_get_absolute_url(self):
        g = Gymnasium(**self.dict)
        g.save()
        self.assertEqual(g.get_absolute_url(), "/gymnasium/watteau/")
