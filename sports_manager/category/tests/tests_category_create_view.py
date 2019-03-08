#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import create_user


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
        }

        r = self.client.post(reverse('sports-manager:category-create'), d)

        self.assertEqual(r.status_code, 403)


class TestCategoryCreateViewAsLogged(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user()[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-create'))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-create'), d)

        self.assertEqual(r.status_code, 403)


class TestCategoryCreateViewAsStaff(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(staff=True)[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)


class TestCategoryCreateViewAsSuperuser(TestCase):
    """Tests CreateView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(superuser=True)[0]

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-create'))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'name': 'Hello World',
            'min_age': 18,
            'summary': 'TODO',
            'description': '# TODO',
        }

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn("hello-world", r.url)
