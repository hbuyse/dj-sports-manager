#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import CategoryHelper, create_user


class TestCategoryDeleteViewAsAnonymous(TestCase):
    """Tests DeleteView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'not-existing'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 403)


class TestCategoryDeleteViewAsLogged(TestCase):
    """Tests DeleteView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}),
                             dict(self.category))

        self.assertEqual(r.status_code, 403)


class TestCategoryDeleteViewAsStaff(TestCase):
    """Tests DeleteView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:category-list'))


class TestCategoryDeleteViewAsSuperuser(TestCase):
    """Tests DeleteView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.category = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.category.object)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:category-delete', kwargs={'slug': self.category.object.slug}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:category-list'))
