# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsGymnasium(TestCase):
    """Tests the urls for the gymnasiums."""

    def test_list_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-list')
        self.assertEqual(url, '/gymnasium/')

    def test_create_url(self):
        """Test the URL of that allows the creation of a post."""
        url = reverse('sports-manager:gymnasium-create')
        self.assertEqual(url, '/gymnasium/create/')

    def test_detail_url(self):
        """Test the URL that gives the details of a post."""
        url = reverse('sports-manager:gymnasium-detail', kwargs={'slug': slugify('Hello World')})
        self.assertEqual(url, '/gymnasium/hello-world/')

    def test_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-update', kwargs={'slug': slugify('Hello World')})
        self.assertEqual(url, "/gymnasium/hello-world/update/")

    def test_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-delete', kwargs={'slug': slugify('Hello World')})
        self.assertEqual(url, "/gymnasium/hello-world/delete/")
