#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Standard library
from datetime import date

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

# Current django project
from sports_manager.player.models import Player
from sports_manager.tests.helper import PlayerHelper, UserHelper


class TestPlayerDeleteViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_owner = UserHelper(username='tata')
        cls.other_player = PlayerHelper(owner=cls.other_owner)
        cls.other_player.create()

    def test_get_player_other_owner_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_player_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_player_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestPlayerDeleteViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper()
        cls.other_owner = UserHelper(username='tata')
        cls.player = PlayerHelper(owner=cls.user.object)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other_owner.object)
        cls.other_player.create()

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertRedirects(r, reverse('sports-manager:player-list',
                                        kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)


class TestPlayerDeleteViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_staff=True)
        cls.other_owner = UserHelper(username='tata')
        cls.player = PlayerHelper(owner=cls.user.object)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other_owner.object)
        cls.other_player.create()

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertRedirects(r, reverse('sports-manager:player-list',
                                        kwargs={'username': self.other_owner.get_username()}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertRedirects(r, reverse('sports-manager:player-list',
                                        kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)


class TestPlayerDeleteViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_superuser=True)
        cls.other_owner = UserHelper(username='tata')
        cls.player = PlayerHelper(owner=cls.user.object)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other_owner.object)
        cls.other_player.create()

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-delete',
                                    kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': 'helloworld', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertRedirects(r, reverse('sports-manager:player-list',
                                        kwargs={'username': self.other_owner.get_username()}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-delete',
                                     kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertRedirects(r, reverse('sports-manager:player-list',
                                        kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)
