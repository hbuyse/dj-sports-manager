#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import EmergencyContact, EmergencyContactHelper, PlayerHelper, UserHelper


class TestEmergencyContactDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='user')
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        if 'one_contact' in test_name:
            if 'wrong_account' in test_name:
                self.contact = EmergencyContactHelper(player=self.other_player)
                self.contact.create()

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 403)


class TestEmergencyContactDetailViewAsLogged(TestCase):
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
        if 'one_contact' in test_name:
            self.contact = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.contact.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 403)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 200)


class TestEmergencyContactDetailViewAsStaff(TestCase):
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
        if 'one_contact' in test_name:
            self.contact = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.contact.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 200)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 200)


class TestEmergencyContactDetailViewAsSuperuser(TestCase):
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
        if 'one_contact' in test_name:
            self.contact = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.contact.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 200)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-detail',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.contact.get('pk')}))
        self.assertEqual(r.status_code, 200)
