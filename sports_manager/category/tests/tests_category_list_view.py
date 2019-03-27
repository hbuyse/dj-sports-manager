#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.category.models import Category
from sports_manager.tests.helper import CategoryHelper, create_user


class TestCategoryListViewAsAnonymous(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        if self.id().split('.')[-1] == 'test_one_category':
            self.helper = CategoryHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def test_one_category(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(self.helper.object, r.context['category_list'])


class TestCategoryListViewAsLogged(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user()[0]
        if self.id().split('.')[-1] == 'test_one_category':
            self.helper = CategoryHelper()
            self.helper.create()


    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def test_one_category(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(self.helper.object, r.context['category_list'])


class TestCategoryListViewAsStaff(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(staff=True)[0]
        if self.id().split('.')[-1] == 'test_one_category':
            self.helper = CategoryHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def test_one_category(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(self.helper.object, r.context['category_list'])


class TestCategoryListViewAsSuperuser(TestCase):
    """Tests ListView for Category."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info = create_user(superuser=True)[0]
        if self.id().split('.')[-1] == 'test_one_category':
            self.helper = CategoryHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 0)

    def test_one_category(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:category-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['category_list']), 1)
        self.assertIn(self.helper.object, r.context['category_list'])
