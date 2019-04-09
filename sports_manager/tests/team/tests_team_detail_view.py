#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TeamHelper, UserHelper


class TestTeamDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)


class TestTeamDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)


class TestTeamDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_staff=True)
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)


class TestTeamDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_superuser=True)
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)
