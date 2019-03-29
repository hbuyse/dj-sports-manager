#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from datetime import date, timedelta
from unittest.mock import MagicMock, PropertyMock

# Django
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.player.models import MedicalCertificate
from sports_manager.tests.helper import PlayerHelper, UserHelper


class TestMedicalCertificateUpdateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='user')
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        if 'wrong_account' in test_name:
            self.form_data = {
                'file': None,
                'start': date.today(),
                'end': date.today() + timedelta(weeks=52),
                'validation': MedicalCertificate.IN_VALIDATION,
            }
            self.form_data['player'] = self.other_player
            self.form_data['file'] = MagicMock(spec=File, size=1 << 20)
            type(self.form_data['file']).name = PropertyMock(return_value='file.pdf')  # Create the mock for file.name

    def test_get_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}),
                             self.form_data)
        self.assertEqual(r.status_code, 403)


class TestMedicalCertificateUpdateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper()
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        self.form_data = {
            'file': None,
            'start': date.today(),
            'end': date.today() + timedelta(weeks=52),
            'validation': MedicalCertificate.IN_VALIDATION,
        }
        self.form_data['player'] = self.other_player if 'wrong_account' in self.id().split('.')[-1] else self.player
        self.form_data['file'] = MagicMock(spec=File, size=1 << 20)
        type(self.form_data['file']).name = PropertyMock(return_value='file.pdf')  # Create the mock for file.name

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_get_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}),
                             self.form_data)
        self.assertEqual(r.status_code, 403)

    def test_post_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}),
                             self.form_data)
        self.assertRedirects(
            r,
            '/{}/player/{}/medical-certificate/1/'.format(self.user.get_username(), self.player.get('slug')),
            fetch_redirect_response=False
        )


class TestMedicalCertificateUpdateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper(is_staff=True)
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        self.form_data = {
            'file': None,
            'start': date.today(),
            'end': date.today() + timedelta(weeks=52),
            'validation': MedicalCertificate.IN_VALIDATION,
        }
        self.form_data['player'] = self.other_player if 'wrong_account' in self.id().split('.')[-1] else self.player
        self.form_data['file'] = MagicMock(spec=File, size=1 << 20)
        type(self.form_data['file']).name = PropertyMock(return_value='file.pdf')  # Create the mock for file.name

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}),
                             self.form_data)
        self.assertRedirects(
            r,
            '/{}/player/{}/medical-certificate/1/'.format(self.other.get_username(),self.other_player.get('slug')),
            fetch_redirect_response=False
        )

    def test_post_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}),
                             self.form_data)
        self.assertRedirects(
            r,
            '/{}/player/{}/medical-certificate/1/'.format(self.user.get_username(), self.player.get('slug')),
            fetch_redirect_response=False
        )


class TestMedicalCertificateUpdateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper(is_superuser=True)
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        self.form_data = {
            'file': None,
            'start': date.today(),
            'end': date.today() + timedelta(weeks=52),
            'validation': MedicalCertificate.IN_VALIDATION,
        }
        self.form_data['player'] = self.other_player if 'wrong_account' in self.id().split('.')[-1] else self.player
        self.form_data['file'] = MagicMock(spec=File, size=1 << 20)
        type(self.form_data['file']).name = PropertyMock(return_value='file.pdf')  # Create the mock for file.name

        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_get_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-create',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}),
                             self.form_data)
        self.assertRedirects(
            r,
            '/{}/player/{}/medical-certificate/1/'.format(self.other.get_username(), self.other_player.get('slug')),
            fetch_redirect_response=False
        )

    def test_post_right_account_player_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}),
                             self.form_data)
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-create',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}),
                             self.form_data)
        self.assertRedirects(
            r,
            '/{}/player/{}/medical-certificate/1/'.format(self.user.get_username(), self.player.get('slug')),
            fetch_redirect_response=False
        )
