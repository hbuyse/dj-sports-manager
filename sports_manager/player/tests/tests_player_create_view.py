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
from sports_manager.tests.helper import UserHelper


class TestPlayerCreateViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_owner = UserHelper(username='tata')
        cls.datas = {
            'first_name': 'Toto',
            'last_name': 'Toto',
            'birthday': date.today(),
            'sex': Player.SEX_FEMALE,
            'address': 'Toto',
            'zip_code': 'Toto',
            'city': 'Toto',
        }

    def test_get_player_other_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_other_owner_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        r = self.client.get(reverse('sports-manager:player-create',
                                    kwargs={'username': self.other_owner.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}), self.datas)
        self.assertEqual(r.status_code, 403)

    def test_post_player_other_owner_existing(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.other_owner.get_username()}), self.datas)
        self.assertEqual(r.status_code, 403)


class TestPlayerCreateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper()
        cls.other_owner = UserHelper(username='tata')
        cls.datas = {
            'first_name': 'Toto',
            'last_name': 'Toto',
            'birthday': date.today(),
            'sex': Player.SEX_FEMALE,
            'address': 'Toto',
            'zip_code': 'Toto',
            'city': 'Toto',
        }
        cls.datas['slug'] = slugify('{} {}'.format(cls.datas['first_name'], cls.datas['last_name']))

    def test_get_player_other_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create',
                                    kwargs={'username': self.other_owner.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_get_player_user_same_as_owner(self):
        """Access a player create view with future owner same as the user logged in.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}), self.datas)
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_existing(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.other_owner.get_username()}), self.datas)
        self.assertEqual(r.status_code, 403)

    def test_post_player_user_same_as_owner(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.user.get_username()}), self.datas)
        self.assertRedirects(r, '/{}/player/{}/'.format(self.user.get_username(),
                                                        self.datas['slug']), fetch_redirect_response=False)


class TestPlayerCreateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_staff=True)
        cls.other_owner = UserHelper(username='tata')
        cls.datas = {
            'first_name': 'Toto',
            'last_name': 'Toto',
            'birthday': date.today(),
            'sex': Player.SEX_FEMALE,
            'address': 'Toto',
            'zip_code': 'Toto',
            'city': 'Toto',
        }
        cls.datas['slug'] = slugify('{} {}'.format(cls.datas['first_name'], cls.datas['last_name']))

    def test_get_player_other_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create',
                                    kwargs={'username': self.other_owner.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_same_as_owner(self):
        """Access a player create view with future owner same as the user logged in.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}), self.datas)
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_existing(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.other_owner.get_username()}), self.datas)
        self.assertRedirects(r, '/{}/player/{}/'.format(self.other_owner.get_username(),
                                                        self.datas['slug']), fetch_redirect_response=False)

    def test_post_player_user_same_as_owner(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.user.get_username()}), self.datas)
        self.assertRedirects(r, '/{}/player/{}/'.format(self.user.get_username(),
                                                        self.datas['slug']), fetch_redirect_response=False)


class TestPlayerCreateViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpClass(cls):
        """Setup for al the following tests."""
        super().setUpClass()
        cls.user = UserHelper(is_superuser=True)
        cls.other_owner = UserHelper(username='tata')
        cls.datas = {
            'first_name': 'Toto',
            'last_name': 'Toto',
            'birthday': date.today(),
            'sex': Player.SEX_FEMALE,
            'address': 'Toto',
            'zip_code': 'Toto',
            'city': 'Toto',
        }
        cls.datas['slug'] = slugify('{} {}'.format(cls.datas['first_name'], cls.datas['last_name']))

    def test_get_player_other_owner_not_existing(self):
        """Access a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}))
        self.assertEqual(r.status_code, 404)

    def test_get_player_other_owner_existing(self):
        """Access a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create',
                                    kwargs={'username': self.other_owner.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_get_player_user_same_as_owner(self):
        """Access a player create view with future owner same as the user logged in.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:player-create', kwargs={'username': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_player_other_owner_not_existing(self):
        """Post datas to a player create view with an owner not existing.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create', kwargs={'username': 'helloworld'}), self.datas)
        self.assertEqual(r.status_code, 404)

    def test_post_player_other_owner_existing(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.other_owner.get_username()}), self.datas)
        self.assertRedirects(r, '/{}/player/{}/'.format(self.other_owner.get_username(),
                                                        self.datas['slug']), fetch_redirect_response=False)

    def test_post_player_user_same_as_owner(self):
        """Post datas to a player create view with an existing owner.

        We should get a 403 error since the 'test_func' kicks in first.
        """
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:player-create',
                                     kwargs={'username': self.user.get_username()}), self.datas)
        self.assertRedirects(r, '/{}/player/{}/'.format(self.user.get_username(),
                                                        self.datas['slug']), fetch_redirect_response=False)
