#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import create_team, create_time_slot, create_user


class TestTeamTimeSlotDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_get_time_slot_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)

    def test_get_time_slot_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_get_time_slot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)


class TestTeamTimeSlotDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.team = create_team()[1]
        self.timeslot_info, self.timeslot = create_time_slot(team=self.team)

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug + 'a', 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 404)

    def test_get_time_slot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk + 1}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.team.slug, 'pk': self.timeslot.pk}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.timeslot)
