#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-sponsoring` apps module."""

from dj_sports_manager.apps import DjSportsManagerConfig

from django.apps import apps
from django.test import TestCase


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(DjSportsManagerConfig.name, 'dj_sports_manager')
        self.assertEqual(apps.get_app_config('dj_sports_manager').name, 'dj_sports_manager')
