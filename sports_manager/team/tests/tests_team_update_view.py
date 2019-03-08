#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.team.models import Team
from sports_manager.tests.helper import create_team, create_user


class TestTeamUpdateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.team_info, self.team = create_team()

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': 'not-existing'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.team_info['name'] = self.team_info['name'] + " New"
        self.team_info['category'] = self.team_info['category'].id

        r = self.client.post(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}),
                             self.team_info)

        self.assertEqual(r.status_code, 403)


class TestTeamUpdateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.team_info, self.team = create_team()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.team_info['name'] = self.team_info['name'] + " New"
        self.team_info['category'] = self.team_info['category'].id

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}),
                             self.team_info)

        self.assertEqual(r.status_code, 403)


class TestTeamUpdateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.team_info, self.team = create_team()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.team)

    def test_post(self):
        """Tests."""
        self.team_info['name'] = self.team_info['name'] + " New"
        self.team_info['category'] = self.team_info['category'].id

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}),
                             self.team_info)

        self.assertEqual(r.status_code, 302)

        self.team = Team.objects.get(pk=self.team.pk)

        self.assertEqual(r.url, reverse('sports-manager:team-detail', kwargs={'slug': self.team.slug}))
        self.assertIn("-new", self.team.slug)


class TestTeamUpdateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.team_info, self.team = create_team()

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['team'], self.team)

    def test_post(self):
        """Tests."""
        self.team_info['name'] = self.team_info['name'] + " New"
        self.team_info['category'] = self.team_info['category'].id

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-update', kwargs={'slug': self.team.slug}),
                             self.team_info)

        self.assertEqual(r.status_code, 302)

        self.team = Team.objects.get(pk=self.team.pk)

        self.assertEqual(r.url, reverse('sports-manager:team-detail', kwargs={'slug': self.team.slug}))
        self.assertIn("-new", self.team.slug)
