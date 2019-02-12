# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


class TestUrlsCategory(TestCase):
    """Tests the urls for the sports-manager."""

    def test_category_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:categorie-list')
        self.assertEqual(url, '/category/')

    def test_category_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-create')
        self.assertEqual(url, '/category/create/')

    def test_category_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:category-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/category/toto/')

    def test_category_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:category-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/category/hello-world/')

    def test_category_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/update/")

    def test_category_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:category-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/category/toto/delete/")


class TestUrlsTeam(TestCase):
    """Tests the urls for the sports-manager."""

    def test_teams_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-list')
        self.assertEqual(url, '/team/')

    def test_team_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-create')
        self.assertEqual(url, '/team/create/')

    def test_team_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Toto")})
        self.assertEqual(url, '/team/toto/')

    def test_team_detail_url_complex(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Hello World")})
        self.assertEqual(url, '/team/hello-world/')

    def test_team_detail_url_complex_2(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('sports-manager:team-detail', kwargs={'slug': slugify("Drunk'n Monkey")})
        self.assertEqual(url, '/team/drunkn-monkey/')

    def test_team_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/update/")

    def test_team_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/team/toto/delete/")


class TestUrlsTimeSlot(TestCase):
    """Tests the urls for the sports-manager."""

    def test_time_slots_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-list', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/')

    def test_time_slot_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-create', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/team/toto/time-slot/create/')

    # def test_time_slot_detail_url_simple(self):
    #     """Test the URL of that allows the creation of a VCN account."""
    #     url = reverse('sports-manager:team-time-slot-detail', kwargs={'slug': 'toto', 'pk': 1})
    #     self.assertEqual(url, '/team/toto/time-slot/1/')

    def test_time_slot_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-update', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/update/")

    def test_time_slot_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('sports-manager:team-time-slot-delete', kwargs={'slug': 'toto', 'pk': 1})
        self.assertEqual(url, "/team/toto/time-slot/1/delete/")


class TestUrlsLicense(TestCase):
    """Tests the urls for the sports-manager."""

    def test_licenses_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            url = reverse('sports-manager:license-list')

        url = reverse('sports-manager:license-list', kwargs={'username': "toto"})
        self.assertEqual(url, '/toto/license/')

    def test_license_create_url(self):
        """Test the URL of the listing of VCN accounts."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            url = reverse('sports-manager:license-create')

        url = reverse('sports-manager:license-create', kwargs={'username': "toto"})
        self.assertEqual(url, '/toto/license/create/')

    def test_license_detail_url_simple(self):
        """Test the URL of that allows the creation of a VCN account."""
        import django
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            for k, v in {'pk': 123456, 'username': "toto"}:
                url = reverse('sports-manager:license-create', kwargs={k: v})

        url = reverse('sports-manager:license-detail', kwargs={'number': 123456, 'username': "toto"})
        self.assertEqual(url, '/toto/license/123456/')

    # def test_license_update_url(self):
    #     """Test the URL of the listing of VCN accounts."""
    #     url = reverse('sports-manager:license-update', kwargs={'number': 123456, 'username': "toto"})
    #     self.assertEqual(url, "/toto/license/123456/update/")

    # def test_license_delete_url(self):
    #     """Test the URL of the listing of VCN accounts."""
    #     url = reverse('sports-manager:license-delete', kwargs={'number': 123456, 'username': "toto"})
    #     self.assertEqual(url, "/toto/license/123456/delete/")

class TestUrlsPost(TestCase):
    """Tests the urls for the gymnasiums."""

    def test_post_list_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-list')
        self.assertEqual(url, '/gymnasium/')

    def test_post_create_url(self):
        """Test the URL of that allows the creation of a post."""
        url = reverse('sports-manager:gymnasium-create')
        self.assertEqual(url, '/gymnasium/create/')

    def test_post_detail_url(self):
        """Test the URL that gives the details of a post."""
        url = reverse('sports-manager:gymnasium-detail', kwargs={'slug': 'hello-world'})
        self.assertEqual(url, '/gymnasium/hello-world/')

    def test_post_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-update', kwargs={'slug': 'hello-world'})
        self.assertEqual(url, "/gymnasium/hello-world/update/")

    def test_post_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('sports-manager:gymnasium-delete', kwargs={'slug': 'hello-world'})
        self.assertEqual(url, "/gymnasium/hello-world/delete/")
