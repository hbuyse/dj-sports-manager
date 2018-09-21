#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .helper import create_category


class TestCategoryDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)


class TestCategoryDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**self.user_info)
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)


class TestCategoryDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        get_user_model().objects.create_user(**self.user_info)
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)


class TestCategoryDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        get_user_model().objects.create_superuser(**self.user_info)
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:category-detail', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)
