#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TimeSlotHelper, create_user


class TestTeamTimeSlotDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.helper = TimeSlotHelper()

    def test_get_team_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug + 'a', 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_time_slot_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user()[0]
        self.helper = TimeSlotHelper()

    def test_get_team_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug + 'a', 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_time_slot_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(staff=True)[0]
        self.helper = TimeSlotHelper()

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug + 'a', 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_time_slot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.helper.object)


class TestTeamTimeSlotDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user_info = create_user(superuser=True)[0]
        self.helper = TimeSlotHelper()

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug + 'a', 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_time_slot_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-detail', kwargs={'team': self.helper.get('team').slug, 'pk': self.helper.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['timeslot'], self.helper.object)
