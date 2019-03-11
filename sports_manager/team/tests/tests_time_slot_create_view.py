#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
import sports_manager
from sports_manager.team.models import TimeSlot
from sports_manager.tests.helper import create_gymnasium, create_team, create_time_slot, create_user


class TestTeamTimeSlotCreateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Set up the tests."""
        self.team = create_team()[1]
        gymnasium = create_gymnasium()[1]
        self.timeslot_info = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Tests."""
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}), self.timeslot_info)
        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Tests."""

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}), self.timeslot_info)

        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotCreateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.team = create_team()[1]
        gymnasium = create_gymnasium()[1]
        self.timeslot_info = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}))

        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}), self.timeslot_info)
        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}), self.timeslot_info)
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotCreateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.team = create_team()[1]
        gymnasium = create_gymnasium()[1]
        self.timeslot_info = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}), self.timeslot_info)
        self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}), self.timeslot_info)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.slug))


class TestTeamTimeSlotCreateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.team = create_team()[1]
        gymnasium = create_gymnasium()[1]
        self.timeslot_info = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'

        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug + 'a'}), self.timeslot_info)
        self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        self.timeslot_info['gymnasium'] = 1
        self.timeslot_info['start'] = '20:00:00'
        self.timeslot_info['end'] = '23:00:00'
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.slug}), self.timeslot_info)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.slug))
