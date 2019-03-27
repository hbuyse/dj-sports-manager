#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import CategoryHelper, create_user


class TestCategoryDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)


class TestCategoryDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)


class TestCategoryDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)


class TestCategoryDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-detail', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)
