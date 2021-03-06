#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

from ..helper import create_category, create_user


class TestCategoryUpdateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'not-existing'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}),
                             **self.category_info)

        self.assertEqual(r.status_code, 403)


class TestCategoryUpdateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}),
                             **self.category_info)

        self.assertEqual(r.status_code, 403)


class TestCategoryUpdateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:category-list'))


class TestCategoryUpdateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.category_info, self.category = create_category()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.slug}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:category-list'))
