#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import PlayerHelper, UserHelper


class TestPlayerDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.player = PlayerHelper(owner=self.user.object)

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestPlayerDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.player = PlayerHelper(owner=self.user.object)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player.object)


class TestPlayerDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.player = PlayerHelper(owner=self.user.object)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player.object)


class TestPlayerDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.player = PlayerHelper(owner=self.user.object)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-detail',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player.object)
