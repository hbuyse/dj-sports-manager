#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import CategoryHelper, UserHelper


class TestTeamCreateViewAsAnonymous(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = CategoryHelper()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.get('id'),
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
        self.category = CategoryHelper()
        self.user = UserHelper()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.get('id'),
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 403)


class TestTeamCreateViewAsStaff(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = CategoryHelper()
        self.user = UserHelper(is_staff=True)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.get('id'),
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)


class TestTeamCreateViewAsSuperuser(TestCase):
    """Tests CreateView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.category = CategoryHelper()
        self.user = UserHelper(is_superuser=True)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'category': self.category.get('pk'),
            'name': 'Hello World Team',
            'level': 'GOL',
            'sex': 'MI',
            'url': 'http://example.com',
            'description': '# TODO',
            'is_recruiting': True,
        }

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)
