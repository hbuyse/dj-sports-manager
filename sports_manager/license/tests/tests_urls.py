# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsLicense(TestCase):
    """Tests the urls for the sports-manager."""

    def test_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            url = reverse('sports-manager:license-list')

        url = reverse('sports-manager:license-list', kwargs={'username': "toto"})
        self.assertEqual(url, '/toto/license/')

    def test_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            url = reverse('sports-manager:license-create')

        url = reverse('sports-manager:license-create', kwargs={'username': "toto"})
        self.assertEqual(url, '/toto/license/create/')

    def test_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            d = {'pk': 123456, 'username': "toto"}
            for k, v in d.items():
                url = reverse('sports-manager:license-create', kwargs={k: v})

        url = reverse('sports-manager:license-detail', kwargs={'pk': 123456, 'username': "toto"})
        self.assertEqual(url, '/toto/license/123456/')

    # def test_update_url(self):
    #     """Test the URL of the listing of VCN accounts."""
    #     url = reverse('sports-manager:license-update', kwargs={'number': 123456, 'username': "toto"})
    #     self.assertEqual(url, "/toto/license/123456/update/")

    # def test_delete_url(self):
    #     """Test the URL of the listing of VCN accounts."""
    #     url = reverse('sports-manager:license-delete', kwargs={'number': 123456, 'username': "toto"})
    #     self.assertEqual(url, "/toto/license/123456/delete/")
