#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.player.models import Player
from sports_manager.tests.helper import EmergencyContactHelper, PlayerHelper, UserHelper


class TestEmergencyContactListViewAsAnonymous(TestCase):
    """Tests ListView for Team."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.user = UserHelper(username='other')
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()
        cls.certif = EmergencyContactHelper(player=cls.player)
        cls.certif.create()
    
    def setUp(self):
        test_name = self.id().split('.')[-1]
        if 'wrong_account' in test_name and 'one_contact' in test_name:
            self.certif = EmergencyContactHelper(player=self.player)
            self.certif.create()

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestEmergencyContactListViewAsLogged(TestCase):
    """Tests ListView for Team."""

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
            self.certif = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 0)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 1)


class TestEmergencyContactListViewAsStaff(TestCase):
    """Tests ListView for Team."""

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
            self.certif = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 0)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 1)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 0)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 1)


class TestEmergencyContactListViewAsSuperuser(TestCase):
    """Tests ListView for Team."""

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
            self.certif = EmergencyContactHelper(player=self.other_player if 'wrong_account' in test_name else self.player)
            self.certif.create()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_wrong_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_wrong_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 0)

    def test_wrong_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 1)

    def test_right_account_player_not_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_not_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_right_account_player_existing_no_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 0)

    def test_right_account_player_existing_one_contact(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-emergency-contact-list', kwargs={'username': self.user.get_username(), 'player': self.player.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['emergencycontact_list']), 1)
