#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

from sports_manager.tests.helper import create_team, create_time_slot, create_user


class TestTimeSlotListViewAsAnonymous(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a team."""
        self.team = create_team()[1]

    def tests_empty(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def tests_one_team(self):
        """Tests."""
        ts = create_time_slot(team=self.team)[1]

        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(ts, r.context['timeslot_list'])


class TestTimeSlotListViewAsLogged(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user()
        self.team = create_team()[1]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def tests_one_team(self):
        """Tests."""
        ts = create_time_slot(team=self.team)[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(ts, r.context['timeslot_list'])


class TestTimeSlotListViewAsStaff(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user(staff=True)
        self.team = create_team()[1]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def tests_one_team(self):
        """Tests."""
        ts = create_time_slot(team=self.team)[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(ts, r.context['timeslot_list'])


class TestTimeSlotListViewAsSuperuser(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user(superuser=True)
        self.team = create_team()[1]

    def tests_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def tests_one_team(self):
        """Tests."""
        ts = create_time_slot(team=self.team)[1]

        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'slug': self.team.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(ts, r.context['timeslot_list'])
