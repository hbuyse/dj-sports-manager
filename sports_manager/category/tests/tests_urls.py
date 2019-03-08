# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsCategory(TestCase):
    """Tests the urls for the sports-manager."""

    def test_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-list')
        self.assertEqual(url, '/category/')

    def test_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-create')
        self.assertEqual(url, '/category/create/')

    def test_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:category-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/category/toto/')

    def test_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:category-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/category/hello-world/')

    def test_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/update/")

    def test_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/delete/")
