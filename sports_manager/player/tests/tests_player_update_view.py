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


class TestPlayerUpdateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other = UserHelper(username='other')
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def test_get_player_other_owner_not_existing(self):
        """Access a player update view with an non existent user and a existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_player_not_existing(self):
        """Access a player update view with an existing owner and a non existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_and_player_existing(self):
        """Access a player update view with an existing owner and a existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to  a player update view with an non existent user and a existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}), dict(self.other_player))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_player_not_existing(self):
        """Post datas to  a player update view with an existing owner and a non existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug') + 'a'}), dict(self.other_player))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_and_player_existing(self):
        """Post datas to  a player update view with an existing owner and a existent player.
        
        Get a 403 status code because an anonymous user does not have the right to watch someone's pages.
        """
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}), dict(self.other_player))
        self.assertEqual(r.status_code, 403)


class TestPlayerUpdateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper()
        cls.other = UserHelper(username='other')
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def test_get_player_other_owner_not_existing(self):
        """Access a player update view with a normal user logged in, a non other existent user and a existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_player_not_existing(self):
        """Access a player update view with a normal user logged in, an other existent user and a non existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_and_player_existing(self):
        """Access a player update view with a normal user logged in, an other existent user and its existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_user_player_not_existing(self):
        """Access a player update view with a normal user logged in, an other existent user and its existent player.
        
        Get a 404 status code because the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Access a player update view with a normal user logged in, the same user and its existent player.
        
        Get a 200 status code because every data is good.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player update view with a normal user logged in, a non other existent user and a existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}), dict(self.other_player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_player_not_existing(self):
        """Post datas to a player update view with a normal user logged in, an other existent user and a non existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug') + 'a'}), dict(self.other_player.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_and_player_existing(self):
        """Post datas to a player update view with a normal user logged in, an other existent user and its existent player.
        
        Get a 403 status code because an normal user does not have the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.player.get('slug')}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_player_user_player_not_existing(self):
        """Post datas to a player update view with a normal user logged in, an other existent user and its existent player.
        
        Get a 404 status code because the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Post datas to a player update view with a normal user logged in, the same user and its existent player.
        
        Get a 302 status code because every data is good. We are redirected to the player detail view.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        self.player.last_name += 'a'
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}), dict(self.player.datas_for_form))
        self.assertRedirects(r, reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), fetch_redirect_response=False)


class TestPlayerUpdateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_staff=True)
        cls.other = UserHelper(username='other')
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def test_get_player_other_owner_not_existing(self):
        """Access a player update view with a staff user logged in, a non other existent user and a existent player.
        
        Get a 404 status code because an staff user has the right to watch someone's pages but the other user slug does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_player_not_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and a non existent player.
        
        Get a 404 status code because an staff user has the right to watch someone's pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_and_player_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 200 status code because an staff user has the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 404 status code because an staff user has the right to watch its pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Access a player update view with a staff user logged in, the same user and its existent player.
        
        Get a 200 status code because an staff user has the right to watch its pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player update view with a staff user logged in, a non other existent user and a existent player.
        
        Get a 404 status code because an staff user has the right to post datas on someone's pages but the other user slug does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_player_not_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and a non existent player.
        
        Get a 404 status code because an staff user has the right to post datas on someone's pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.player.get('slug') + 'a'}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_and_player_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 200 status code because an staff user has the right to post datas on someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}), dict(self.player.datas_for_form))
        self.assertRedirects(r, reverse('sports-manager:player-detail', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 404 status code because an staff user has the right to post datas on its pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Post datas to a player update view with a staff user logged in, the same user and its existent player.
        
        Get a 404 status code because an staff user has the right to post datas on its pages and every datas is good.
        We are redirected to the player detail view.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        self.player.last_name += 'a'
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}), dict(self.player.datas_for_form))
        self.assertRedirects(r, reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), fetch_redirect_response=False)


class TestPlayerUpdateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_superuser=True)
        cls.other = UserHelper(username='other')
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def test_get_player_other_owner_not_existing(self):
        """Access a player update view with a staff user logged in, a non other existent user and a existent player.
        
        Get a 404 status code because an staff user has the right to watch someone's pages but the other user slug does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_player_not_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and a non existent player.
        
        Get a 404 status code because an staff user has the right to watch someone's pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_and_player_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 200 status code because an staff user has the right to watch someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_player_not_existing(self):
        """Access a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 404 status code because an staff user has the right to watch its pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_user_owner_and_player_existing(self):
        """Access a player update view with a staff user logged in, the same user and its existent player.
        
        Get a 200 status code because an staff user has the right to watch its pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player update view with a staff user logged in, a non other existent user and a existent player.
        
        Get a 404 status code because an staff user has the right to post datas on someone's pages but the other user slug does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username() + 'a', 'slug': self.other_player.get('slug')}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_player_not_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and a non existent player.
        
        Get a 404 status code because an staff user has the right to post datas on someone's pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.player.get('slug') + 'a'}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_and_player_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 200 status code because an staff user has the right to post datas on someone's pages.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}), dict(self.player.datas_for_form))
        self.assertRedirects(r, reverse('sports-manager:player-detail', kwargs={'username': self.other.get_username(), 'slug': self.other_player.get('slug')}), fetch_redirect_response=False)

    def test_post_player_user_player_not_existing(self):
        """Post datas to a player update view with a staff user logged in, an other existent user and its existent player.
        
        Get a 404 status code because an staff user has the right to post datas on its pages but the player does not exist.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), dict(self.player.datas_for_form))
        self.assertEqual(r.status_code, 404)

    def test_post_player_user_owner_and_player_existing(self):
        """Post datas to a player update view with a staff user logged in, the same user and its existent player.
        
        Get a 404 status code because an staff user has the right to post datas on its pages and every datas is good.
        We are redirected to the player detail view.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        self.player.last_name += 'a'
        r = self.client.post(reverse('sports-manager:player-update', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug')}), dict(self.player.datas_for_form))
        self.assertRedirects(r, reverse('sports-manager:player-detail', kwargs={'username': self.user.get_username(), 'slug': self.player.get('slug') + 'a'}), fetch_redirect_response=False)
