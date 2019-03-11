#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import create_team, create_time_slot, create_user


class TestTeamTimeSlotDeleteViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_post_timeslot_not_existing(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDeleteViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_post_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDeleteViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_post_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.slug))


class TestTeamTimeSlotDeleteViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_post_timeslot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.post(reverse('sports-manager:team-time-slot-delete', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.slug))
