#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.category.models import Category
from sports_manager.tests.helper import CategoryHelper, UserHelper


class TestCategoryUpdateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.helper = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': 'not-existing'}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New" 
        r = self.client.post(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}), dict(self.helper))
        self.assertEqual(r.status_code, 403)


class TestCategoryUpdateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.helper = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': 'toto'}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New"
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}), dict(self.helper))
        self.assertEqual(r.status_code, 403)


class TestCategoryUpdateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_staff=True)
        self.helper = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New" 
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}), dict(self.helper))
        self.assertEqual(r.status_code, 302)
        category = Category.objects.get(pk=self.helper.object.pk)
        self.assertEqual(r.url, reverse('sports-manager:category-detail', kwargs={'slug': category.slug}))
        self.assertIn("-new", category.slug)


class TestCategoryUpdateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_superuser=True)
        self.helper = CategoryHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['category'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New" 
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:category-update', kwargs={'slug': self.helper.get('slug')}), dict(self.helper))
        self.assertEqual(r.status_code, 302)
        category = Category.objects.get(pk=self.helper.object.pk)
        self.assertEqual(r.url, reverse('sports-manager:category-detail', kwargs={'slug': category.slug}))
        self.assertIn("-new", category.slug)
