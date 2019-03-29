#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.team.models import Team
from sports_manager.tests.helper import TeamHelper, UserHelper


class TestTeamUpdateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.helper = TeamHelper()
        self.helper.create()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': 'not-existing'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': self.helper.get('slug')}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New"
        r = self.client.post(reverse('sports-manager:team-update',
                                     kwargs={'team': self.helper.get('slug')}), dict(self.helper))
        self.assertEqual(r.status_code, 403)


class TestTeamUpdateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper()
        self.helper = TeamHelper()
        self.helper.create()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': self.helper.get('slug')}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New"
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-update',
                                     kwargs={'team': self.helper.get('slug')}), dict(self.helper))

        self.assertEqual(r.status_code, 403)


class TestTeamUpdateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_staff=True)
        self.helper = TeamHelper()
        self.helper.create()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': self.helper.get('slug')}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New"
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-update',
                                     kwargs={'team': self.helper.get('slug')}), dict(self.helper.datas_for_form))
        self.assertRedirects(r, '/team/{}-new/'.format(self.helper.get('slug')), fetch_redirect_response=False)


class TestTeamUpdateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user = UserHelper(is_superuser=True)
        self.helper = TeamHelper()
        self.helper.create()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'team': self.helper.get('slug')}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)

    def test_post(self):
        """Tests."""
        self.helper.name = self.helper.name + " New"
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-update',
                                     kwargs={'team': self.helper.get('slug')}), dict(self.helper.datas_for_form))
        self.assertRedirects(r, '/team/{}-new/'.format(self.helper.get('slug')), fetch_redirect_response=False)
