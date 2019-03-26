# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.text import slugify

from sports_manager.tests.helper import reload_urlconf


class TestUrlsPlayer(TestCase):
    """Tests the urls for the players."""

    def test_list_url(self):
        """Test the URL of the listing of the players."""
        url = reverse('sports-manager:player-list', kwargs={'username': 'toto'})
        self.assertEqual(url, '/toto/player/')

    def test_create_url(self):
        """Test the URL of that allows the creation of a player."""
        url = reverse('sports-manager:player-create', kwargs={'username': 'toto'})
        self.assertEqual(url, '/toto/player/create/')

    @override_settings(SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE=True)
    def test_create_aio_url(self):
        reload_urlconf()
        """Test the URL of that allows the creation of a player."""
        reload_urlconf('sports_manager.player.urls')
        reload_urlconf('sports_manager.urls')
        reload_urlconf('sports_manager.tests.urls')
        url = reverse('sports-manager:player-create', kwargs={'username': 'toto'})
        self.assertEqual(url, '/toto/player/create/')

    def test_detail_url(self):
        """Test the URL that gives the details of a player."""
        url = reverse('sports-manager:player-detail', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/')

    def test_update_url(self):
        """Test the URL that updates a player."""
        url = reverse('sports-manager:player-update', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, "/toto/player/hello-world/update/")

    @override_settings(SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE=True)
    def test_update_aio_url(self):
        """Test the URL that updates a player."""
        reload_urlconf('sports_manager.player.urls')
        reload_urlconf('sports_manager.urls')
        reload_urlconf('sports_manager.tests.urls')
        url = reverse('sports-manager:player-update', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, "/toto/player/hello-world/update/")

    def test_delete_url(self):
        """Test the URL that deletes a player."""
        url = reverse('sports-manager:player-delete', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, "/toto/player/hello-world/delete/")


class TestUrlsMedicalCertificate(TestCase):
    """Tests the urls for the players."""

    def test_list_url(self):
        """Test the URL of the listing of the players."""
        url = reverse('sports-manager:player-medical-certificate-list', kwargs={'username': 'toto', 'player': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/medical-certificate/')

    def test_create_url(self):
        """Test the URL of that allows the creation of a player."""
        url = reverse('sports-manager:player-medical-certificate-create', kwargs={'username': 'toto', 'player': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/medical-certificate/create/')

    def test_detail_url(self):
        """Test the URL that gives the details of a player."""
        url = reverse('sports-manager:player-medical-certificate-detail', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, '/toto/player/hello-world/medical-certificate/1/')

    def test_update_url(self):
        """Test the URL that updates a player."""
        url = reverse('sports-manager:player-medical-certificate-update', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, "/toto/player/hello-world/medical-certificate/1/update/")

    def test_delete_url(self):
        """Test the URL that deletes a player."""
        url = reverse('sports-manager:player-medical-certificate-delete', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, "/toto/player/hello-world/medical-certificate/1/delete/")

    @override_settings(SPORTS_MANAGER_MEDICAL_CERTIFICATE_MAX_RENEW=3)
    def test_renew_url(self):
        """Test the URL that renews a player."""
        reload_urlconf('sports_manager.player.urls')
        reload_urlconf('sports_manager.urls')
        reload_urlconf('sports_manager.tests.urls')
        url = reverse('sports-manager:player-medical-certificate-renew', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, "/toto/player/hello-world/medical-certificate/1/renew/")


class TestUrlsEmergencyContact(TestCase):
    """Tests the urls for the players."""

    def test_list_url(self):
        """Test the URL of the listing of the players."""
        url = reverse('sports-manager:player-emergency-contact-list', kwargs={'username': 'toto', 'player': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/emergency-contact/')

    def test_create_url(self):
        """Test the URL of that allows the creation of a player."""
        url = reverse('sports-manager:player-emergency-contact-create', kwargs={'username': 'toto', 'player': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/emergency-contact/create/')

    def test_detail_url(self):
        """Test the URL that gives the details of a player."""
        url = reverse('sports-manager:player-emergency-contact-detail', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, '/toto/player/hello-world/emergency-contact/1/')

    def test_update_url(self):
        """Test the URL that updates a player."""
        url = reverse('sports-manager:player-emergency-contact-update', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, "/toto/player/hello-world/emergency-contact/1/update/")

    def test_delete_url(self):
        """Test the URL that deletes a player."""
        url = reverse('sports-manager:player-emergency-contact-delete', kwargs={'username': 'toto', 'player': slugify('Hello World'), 'pk': 1})
        self.assertEqual(url, "/toto/player/hello-world/emergency-contact/1/delete/")
