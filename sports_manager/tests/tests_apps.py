#!/usr/bin/env python
# coding=utf-8

"""
test_dj-sponsoring
------------

Tests for `dj-sponsoring` apps module.
"""

# Django
from django.apps import apps
from django.test import TestCase

# Current django project
from sports_manager.apps import SportsManagerConfig


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(SportsManagerConfig.name, 'sports_manager')
        self.assertEqual(apps.get_app_config('sports_manager').name, 'sports_manager')
