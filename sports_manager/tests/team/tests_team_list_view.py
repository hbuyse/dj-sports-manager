#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TeamHelper, UserHelper


class TestTeamListViewAsAnonymous(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        if self.id().split('.')[-1] == 'test_one_team':
            self.helper = TeamHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 0)

    def test_one_team(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 1)
        self.assertIn(self.helper.object, r.context['team_list'])


class TestTeamListViewAsLogged(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper()
        if self.id().split('.')[-1] == 'test_one_team':
            self.helper = TeamHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 0)

    def test_one_team(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 1)
        self.assertIn(self.helper.object, r.context['team_list'])


class TestTeamListViewAsStaff(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper(is_staff=True)
        if self.id().split('.')[-1] == 'test_one_team':
            self.helper = TeamHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 0)

    def test_one_team(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 1)
        self.assertIn(self.helper.object, r.context['team_list'])


class TestTeamListViewAsSuperuser(TestCase):
    """Tests ListView for Team."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user = UserHelper(is_superuser=True)
        if self.id().split('.')[-1] == 'test_one_team':
            self.helper = TeamHelper()
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 0)

    def test_one_team(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['team_list']), 1)
        self.assertIn(self.helper.object, r.context['team_list'])
