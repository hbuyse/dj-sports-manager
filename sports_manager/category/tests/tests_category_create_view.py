#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from tempfile import NamedTemporaryFile

# Django
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import UserHelper


class TestCategoryCreateViewAsAnonymous(TestCase):
    """Tests CreateView for Category."""

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-create'))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
            'img': NamedTemporaryFile(suffix=".jpg").name
        }

        r = self.client.post(reverse('sports-manager:category-create'), d)
        self.assertEqual(r.status_code, 403)


class TestCategoryCreateViewAsLogged(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-create'))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
            'img': NamedTemporaryFile(suffix=".jpg").name
        }
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-create'), d)
        self.assertEqual(r.status_code, 403)


class TestCategoryCreateViewAsStaff(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper(is_staff=True)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-create'))
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
            'img': NamedTemporaryFile(suffix=".jpg").name
        }
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-create'), d)
        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)


class TestCategoryCreateViewAsSuperuser(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper(is_superuser=True)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-create'))
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
            'img': NamedTemporaryFile(suffix=".jpg").name
        }
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-create'), d)
        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)
