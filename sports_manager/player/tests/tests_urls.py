# coding=utf-8

"""Tests for `sports-manager` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify


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

    def test_detail_url(self):
        """Test the URL that gives the details of a player."""
        url = reverse('sports-manager:player-detail', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, '/toto/player/hello-world/')

    def test_update_url(self):
        """Test the URL that updates a player."""
        url = reverse('sports-manager:player-update', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, "/toto/player/hello-world/update/")

    def test_delete_url(self):
        """Test the URL that deletes a player."""
        url = reverse('sports-manager:player-delete', kwargs={'username': 'toto', 'slug': slugify('Hello World')})
        self.assertEqual(url, "/toto/player/hello-world/delete/")
