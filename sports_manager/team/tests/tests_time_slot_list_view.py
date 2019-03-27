#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.tests.helper import TeamHelper, TimeSlotHelper, create_user


class TestTeamTimeSlotListViewAsAnonymous(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a team."""
        self.team = TeamHelper()
        if self.id().split('.')[-1] == 'test_one_time_slot':
            self.helper = TimeSlotHelper(team=self.team)
            self.helper.create()

    def test_empty(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_one_time_slot(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotListViewAsLogged(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user()
        self.team = TeamHelper()
        if self.id().split('.')[-1] == 'test_one_time_slot':
            self.helper = TimeSlotHelper(team=self.team)
            self.helper.create()

    def test_empty(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_one_time_slot(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotListViewAsStaff(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user(staff=True)
        self.team = TeamHelper()
        if self.id().split('.')[-1] == 'test_one_time_slot':
            self.helper = TimeSlotHelper(team=self.team)
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def test_one_time_slot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(self.helper.object, r.context['timeslot_list'])


class TestTeamTimeSlotListViewAsSuperuser(TestCase):
    """Tests ListView for TimeSlot."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.user_info, self.user = create_user(superuser=True)
        self.team = TeamHelper()
        if self.id().split('.')[-1] == 'test_one_time_slot':
            self.helper = TimeSlotHelper(team=self.team)
            self.helper.create()

    def test_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 0)

    def test_one_time_slot(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.user_info['username'], password=self.user_info['password']))
        r = self.client.get(reverse('sports-manager:team-time-slot-list', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['timeslot_list']), 1)
        self.assertIn(self.helper.object, r.context['timeslot_list'])
