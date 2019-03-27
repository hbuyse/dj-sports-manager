#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TeamHelper, create_user


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
        self.user_info = create_user()[0]
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)


class TestTeamDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)


class TestTeamDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.helper = TeamHelper()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-detail', kwargs={'team': self.helper.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.helper.object)
