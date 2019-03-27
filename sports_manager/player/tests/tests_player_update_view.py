#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from datetime import date

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

# Current django project
from sports_manager.player.models import Player
from sports_manager.tests.helper import create_player, create_user


class TestPlayerUpdateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_owner = create_user(username='tata')[1]
        cls.other_player = create_player(owner=cls.other_owner)[1]

    def test_get_player_other_owner_owner_not_existing(self):
        """Access a player create view with an owner not existing.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_player_not_existing(self):
        """Access a player create view with an owner not existing.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Access a player create view with an existing owner.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_not_existing(self):
        """Access a player create view with an owner not existing.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_player_not_existing(self):
        """Access a player create view with an owner not existing.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Access a player create view with an existing owner.
        
        We should get a 403 status code since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)


class TestPlayerUpdateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user_info, cls.user = create_user()
        cls.other_owner = create_user(username='tata')[1]
        cls.player = create_player(owner=cls.user)[1]
        cls.other_player = create_player(owner=cls.other_owner)[1]

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.player.slug}))
        self.assertRedirects(r, reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)


class TestPlayerUpdateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user_info, cls.user = create_user(staff=True)
        cls.other_owner = create_user(username='tata')[1]
        cls.player = create_player(owner=cls.user)[1]
        cls.other_player = create_player(owner=cls.other_owner)[1]

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertRedirects(r, reverse('sports-manager:player-list', kwargs={'username': self.other_owner.get_username()}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.player.slug}))
        self.assertRedirects(r, reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)


class TestPlayerUpdateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user_info, cls.user = create_user(superuser=True)
        cls.other_owner = create_user(username='tata')[1]
        cls.player = create_player(owner=cls.user)[1]
        cls.other_player = create_player(owner=cls.other_owner)[1]

    def test_get_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Get a 200 status code since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_owner_not_existing(self):
        """Get a 404 status code since we are logged but the user 'other_owner' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': 'helloworld', 'slug': self.other_player.slug}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_player_not_existing(self):
        """Get a 404 status code since the user access other user's pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_owner_and_player_existing(self):
        """Get a 403 status code since we are logged but the user 'other_owner' exists but we do not have the right to view its pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.other_owner.get_username(), 'slug': self.other_player.slug}))
        self.assertRedirects(r, reverse('sports-manager:player-list', kwargs={'username': self.other_owner.get_username()}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Get a 404 status code since the user access its own pages but the 'player' does not exist."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': 'hello-world'}))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Get a 302 status code with redirection since the user access its own player."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:player-delete', kwargs={'username': self.user.get_username(), 'slug': self.player.slug}))
        self.assertRedirects(r, reverse('sports-manager:player-list', kwargs={'username': self.user.get_username()}), fetch_redirect_response=False)
