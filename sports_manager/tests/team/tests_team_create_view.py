#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

from sports_manager.tests.helper import create_category, create_user


class TestTeamCreateViewAsAnonymous(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = create_category()[1]

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.id,
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 403)


class TestTeamCreateViewAsLogged(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = create_category()[1]
        self.user_info = create_user()[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.id,
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 403)


class TestTeamCreateViewAsStaff(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = create_category()[1]
        self.user_info = create_user(staff=True)[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.id,
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)


class TestTeamCreateViewAsSuperuser(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = create_category()[1]
        self.user_info = create_user(superuser=True)[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.id,
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)
