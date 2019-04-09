#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TeamHelper, UserHelper


class TestTeamDeleteViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': 'not-existing'}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestTeamDeleteViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': 'toto'}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestTeamDeleteViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_staff=True)
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:team-list'))


class TestTeamDeleteViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_superuser=True)
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-delete', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('sports-manager:team-list'))
