#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import MedicalCertificateHelper, PlayerHelper, UserHelper


class TestMedicalCertificateDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='user')
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        if 'one_certificate' in test_name:
            if 'wrong_account' in test_name:
                self.certif = MedicalCertificateHelper(player=self.other_player)
                self.certif.create()

    def test_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 403)


class TestMedicalCertificateDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

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
        test_name = self.id().split('.')[-1]
        if 'one_certificate' in test_name:
            self.certif = MedicalCertificateHelper(
                player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 200)


class TestMedicalCertificateDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

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
        test_name = self.id().split('.')[-1]
        if 'one_certificate' in test_name:
            self.certif = MedicalCertificateHelper(
                player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 200)

    def test_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 200)


class TestMedicalCertificateDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

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
        test_name = self.id().split('.')[-1]
        if 'one_certificate' in test_name:
            self.certif = MedicalCertificateHelper(
                player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 200)

    def test_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.get('pk')}))
        self.assertEqual(r.status_code, 200)
