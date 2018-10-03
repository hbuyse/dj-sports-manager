#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-sports-manager` urls module."""

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsCategory(TestCase):
    """Tests the urls for the dj-sports-manager."""

    def test_category_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:categories-list')
        self.assertEqual(url, '/category/')

    def test_category_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:category-create')
        self.assertEqual(url, '/category/create')

    def test_category_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:category-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/category/toto')

    def test_category_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:category-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/category/hello-world')

    def test_category_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:category-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/update")

    def test_category_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:category-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/delete")


class TestUrlsTeam(TestCase):
    """Tests the urls for the dj-sports-manager."""

    def test_teams_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:teams-list')
        self.assertEqual(url, '/team/')

    def test_team_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-create')
        self.assertEqual(url, '/team/create')

    def test_team_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:team-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/team/toto')

    def test_team_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:team-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/team/hello-world')

    def test_team_detail_url_complex_2(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:team-detail', kwargs={'slug': slugify("Drunk'n Monkey")})
        self.assertEqual(url, '/team/drunkn-monkey')

    def test_team_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/update")

    def test_team_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/delete")


class TestUrlsTimeSlot(TestCase):
    """Tests the urls for the dj-sports-manager."""

    def test_time_slots_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-time-slots-list', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/')

    def test_time_slot_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-time-slot-create', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/create')

    def test_time_slot_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, '/team/toto/time-slot/1')

    def test_time_slot_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-time-slot-update', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/update")

    def test_time_slot_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:team-time-slot-delete', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/delete")


class TestUrlsLicense(TestCase):
    """Tests the urls for the dj-sports-manager."""

    def test_licences_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:licenses-list')
        self.assertEqual(url, '/license/')

    def test_license_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:license-create')
        self.assertEqual(url, '/license/create')

    def test_license_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-sports-manager:license-detail', kwargs={'pk': 123456})
        self.assertEqual(url, '/license/123456')

    def test_license_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:license-update', kwargs={'pk': 123456})
        self.assertEqual(url, "/license/123456/update")

    def test_license_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-sports-manager:license-delete', kwargs={'pk': 123456})
        self.assertEqual(url, "/license/123456/delete")
