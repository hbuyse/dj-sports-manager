#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.team.models import TimeSlot
from sports_manager.tests.helper import TeamHelper, UserHelper, GymnasiumHelper


class TestTeamTimeSlotCreateViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpClass(cls):
        """Tests."""
        super().setUpClass()
        cls.team = TeamHelper()
        cls.team.create()
        gymnasium = GymnasiumHelper()
        cls.datas = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.object.pk
        }

    def test_get_team_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}), self.datas)
        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Get a 403 status code because an anonymous user can not access Team's pages so it can not access their time slots pages."""
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}), self.datas)
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotCreateViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpClass(cls):
        """Tests."""
        super().setUpClass()
        cls.user = UserHelper()
        cls.team = TeamHelper()
        cls.team.create()
        gymnasium = GymnasiumHelper()
        cls.datas = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.get('pk')
        }

    def test_get_team_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 403)

    def test_get_timeslot(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 403)

    def test_post_team_not_existing(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}), self.datas)
        self.assertEqual(r.status_code, 403)

    def test_post_timeslot(self):
        """Get a 403 status code because an normal user can not access Team's pages so it can not access their time slots pages."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}), self.datas)
        self.assertEqual(r.status_code, 403)


class TestTeamTimeSlotCreateViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpClass(cls):
        """Tests."""
        super().setUpClass()
        cls.user = UserHelper(is_staff=True)
        cls.team = TeamHelper()
        cls.team.create()
        gymnasium = GymnasiumHelper()
        cls.datas = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.object.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}))
        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}))
        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

        with self.assertRaises(ObjectDoesNotExist):
            r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}), self.datas)
            self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}), self.datas)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.get('slug')))


class TestTeamTimeSlotCreateViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpClass(cls):
        """Tests."""
        super().setUpClass()
        cls.user = UserHelper(is_superuser=True)
        cls.team = TeamHelper()
        cls.team.create()
        gymnasium = GymnasiumHelper()
        cls.datas = {
            'type': TimeSlot.PRACTICE,
            'day': TimeSlot.MONDAY,
            'start': '20:00:00',
            'end': '22:30:00',
            'gymnasium': gymnasium.object.pk
        }

    def test_get_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}))

        self.assertEqual(r.status_code, 404)

    def test_get_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.get(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}))

        self.assertEqual(r.status_code, 200)

    def test_post_team_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

        with self.assertRaises(ObjectDoesNotExist):
            r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug') + 'a'}), self.datas)
            self.assertEqual(r.status_code, 404)

    def test_post_timeslot(self):
        """Tests."""
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))
        r = self.client.post(reverse('sports-manager:team-time-slot-create', kwargs={'team': self.team.get('slug')}), self.datas)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/team/{}/".format(self.team.get('slug')))
