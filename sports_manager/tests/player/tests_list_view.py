#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

from sports_manager.tests.helper import create_player, create_user


class TestPlayerListViewAsAnonymous(TestCase):
    """Tests ListView for Team."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.owner_info, cls.owner = create_user()

    def tests_empty(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 403)

    def tests_one_player(self):
        """Tests."""
        self.player_info, self.player = create_player(owner=self.owner)
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 403)


class TestPlayerListViewAsLogged(TestCase):
    """Tests ListView for Team."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.owner_info, cls.owner = create_user()
        cls.user_info, cls.user = create_user("client")


    def tests_wrong_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 403)

    def tests_wrong_account_one_player(self):
        """Tests."""
        self.player_info, self.player = create_player(owner=self.owner)
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 403)


    def tests_right_account_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.owner_info['username'], password=self.owner_info['password']))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 0)

    def tests_right_account_one_player(self):
        """Tests."""
        self.player_info, self.player = create_player(owner=self.owner)
        self.assertTrue(self.client.login(username=self.owner_info['username'], password=self.owner_info['password']))
        r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['player_list']), 1)


class TestPlayerListViewAsStaff(TestCase):
    """Tests ListView for Team."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.owner_info, cls.owner = create_user()
        cls.user_info, cls.user = create_user("client", staff=True)

    def tests_empty(self):
        """Tests."""
        for info in [self.owner_info, self.user_info]:
            self.assertTrue(self.client.login(username=info['username'], password=info['password']))
            r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['player_list']), 0)

    def tests_one_player(self):
        """Tests."""
        self.player_info, self.player = create_player(owner=self.owner)
        for info in [self.owner_info, self.user_info]:
            self.assertTrue(self.client.login(username=info['username'], password=info['password']))
            r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['player_list']), 1)


class TestPlayerListViewAsSuperuser(TestCase):
    """Tests ListView for Team."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.owner_info, cls.owner = create_user()
        cls.user_info, cls.user = create_user("client", superuser=True)

    def tests_empty(self):
        """Tests."""
        for info in [self.owner_info, self.user_info]:
            self.assertTrue(self.client.login(username=info['username'], password=info['password']))
            r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['player_list']), 0)

    def tests_one_player(self):
        """Tests."""
        self.player_info, self.player = create_player(owner=self.owner)

        for info in [self.owner_info, self.user_info]:
            self.assertTrue(self.client.login(username=info['username'], password=info['password']))
            r = self.client.get(reverse('sports-manager:player-list', kwargs={'username': self.owner.username}))

            self.assertEqual(r.status_code, 200)
            self.assertEqual(len(r.context['player_list']), 1)
