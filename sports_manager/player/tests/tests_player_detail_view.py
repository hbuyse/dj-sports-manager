#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import create_player, create_user


class TestPlayerDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info, self.user = create_user()
        self.player_info, self.player = create_player(self.user)

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': 'toto'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': self.player.slug}))

        self.assertEqual(r.status_code, 403)


class TestPlayerDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info, self.user = create_user()
        self.player_info, self.player = create_player(self.user)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': self.player.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player)


class TestPlayerDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info, self.user = create_user()
        self.player_info, self.player = create_player(self.user)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': self.player.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player)


class TestPlayerDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info, self.user = create_user()
        self.player_info, self.player = create_player(self.user)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(),
                                                                            'slug': self.player.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['player'], self.player)
