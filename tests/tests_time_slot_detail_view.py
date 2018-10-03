#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.test import TestCase
from django.urls import reverse

from .helper import create_user, create_team, create_time_slot


class TestTimeSlotDetailViewAsAnonymous(TestCase):
    """Tests DetailView for TimeSlot."""

    def setUp(self):
        """Tests."""
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail',
                                    kwargs={'slug': 'toto', 'pk': self.timeslot.id})
                            )

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail',
                                    kwargs={'slug': self.team.sug, 'pk': self.timeslot.id})
                            )

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail',
                                    kwargs={'slug': self.timeslot.slug, 'pk': self.timeslot.id})
                            )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)


class TestTimeSlotDetailViewAsLogged(TestCase):
    """Tests DetailView for TimeSlot."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': self.timeslot.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)


class TestTimeSlotDetailViewAsStaff(TestCase):
    """Tests DetailView for TimeSlot."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': self.timeslot.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)


class TestTimeSlotDetailViewAsSuperuser(TestCase):
    """Tests DetailView for TimeSlot."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('dj-sports-manager:team-time-slot-detail', kwargs={'slug': self.timeslot.slug}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)
