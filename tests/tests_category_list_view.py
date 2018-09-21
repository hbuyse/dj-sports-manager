#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.test import TestCase
from django.urls import reverse

from .helper import create_category, create_user


class TestCategoryListViewAsAnonymous(TestCase):
    """Tests ListView for Category."""

    def tests_empty(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def tests_one_category(self):
        """Tests."""
        c = create_category()[1]

        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(c, r.context['category_list'])


class TestCategoryListViewAsLogged(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user()[0]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def tests_one_category(self):
        """Tests."""
        c = create_category()[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(c, r.context['category_list'])


class TestCategoryListViewAsStaff(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(staff=True)[0]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def tests_one_category(self):
        """Tests."""
        c = create_category()[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(c, r.context['category_list'])


class TestCategoryListViewAsSuperuser(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(superuser=True)[0]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def tests_one_category(self):
        """Tests."""
        c = create_category()[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:categories-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(c, r.context['category_list'])
