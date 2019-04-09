#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.models.player import Player
from sports_manager.tests.helper import PlayerHelper, UserHelper


class TestPlayerListViewAsAnonymous(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.other = UserHelper(username='other')
        if self.id().split('.')[-1] == 'test_one_player':
            self.player = PlayerHelper(owner=self.other)
            self.player.create()

    def test_empty(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_one_player(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 403)


class TestPlayerListViewAsLogged(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.other = UserHelper(username='other')
        self.user = UserHelper()
        if 'one_player' in self.id().split('.')[-1]:
            self.player = PlayerHelper(owner=self.other)
            self.player.create()

    def test_wrong_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_right_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def test_right_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)


class TestPlayerListViewAsStaff(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.other = UserHelper(username='other')
        self.user = UserHelper(is_staff=True)
        if 'one_player' in self.id().split('.')[-1]:
            self.player = PlayerHelper(owner=self.other)
            self.player.create()

    def test_wrong_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def test_wrong_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 1)

    def test_right_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def test_right_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)


class TestPlayerListViewAsSuperuser(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.other = UserHelper(username='other')
        self.user = UserHelper(is_superuser=True)
        if 'one_player' in self.id().split('.')[-1]:
            self.player = PlayerHelper(owner=self.other)
            self.player.create()

    def test_wrong_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def test_wrong_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.other.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 1)

    def test_right_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def test_right_account_one_player(self):
        """Tests."""
        self.assertTrue(self.client.login(**dict(self.user.get_credentials())))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)
