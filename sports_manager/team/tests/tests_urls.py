# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsTeam(TestCase):
    """Tests the urls for the sports-manager."""

    def test_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-list')
        self.assertEqual(url, '/team/')

    def test_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-create')
        self.assertEqual(url, '/team/create/')

    def test_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/team/toto/')

    def test_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/team/hello-world/')

    def test_detail_url_complex_2(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Drunk'n Monkey")})
        self.assertEqual(url, '/team/drunkn-monkey/')

    def test_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/update/")

    def test_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/delete/")


class TestUrlsTimeSlot(TestCase):
    """Tests the urls for the sports-manager."""

    def test_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-list', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/')

    def test_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-create', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/create/')

    # def test_detail_url_simple(self):
    #     """Test the URL of that allows the creation of a VCN account."""
    #     url = reverse('sports-manager:team-time-slot-detail', kwargs={'slug': 'toto', 'pk': 1})
    #     self.assertEqual(url, '/team/toto/time-slot/1/')

    def test_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-update', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/update/")

    def test_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-delete', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/delete/")
