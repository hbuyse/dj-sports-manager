#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.models import Gymnasium


class TestGymnasiumUpdateViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.gymnasium_data = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        self.gymnasium = Gymnasium.objects.create(**self.gymnasium_data)
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.gymnasium_data['name'] = 'Watteau2'

        r = self.client.post(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}), self.gymnasium_data)

        self.assertEqual(r.status_code, 403)


class TestGymnasiumUpdateViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**self.dict)

        self.gymnasium_data = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        self.gymnasium = Gymnasium.objects.create(**self.gymnasium_data)
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        self.gymnasium_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}), self.gymnasium_data)

        self.assertEqual(r.status_code, 403)


class TestGymnasiumUpdateViewAsStaff(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        get_user_model().objects.create_user(**self.dict)

        self.gymnasium_data = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        self.gymnasium = Gymnasium.objects.create(**self.gymnasium_data)
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.gymnasium_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}), self.gymnasium_data)

        self.assertRedirects(r, '/gymnasium/watteau2/', fetch_redirect_response=False)


class TestGymnasiumUpdateViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'henri.buyse@gmail.com'
        }
        get_user_model().objects.create_superuser(**self.dict)

        self.gymnasium_data = {
            'name': 'Watteau',
            'address': '37 rue Lequesne',
            'city': 'Nogent-Sur-Marne',
            'zip_code': '94130',
            'phone': '0100000000',
            'surface': '123',
            'capacity': '456',
        }
        self.gymnasium = Gymnasium.objects.create(**self.gymnasium_data)
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.gymnasium_data['name'] = 'Watteau2'

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('sports-manager:gymnasium-update', kwargs={'slug': self.gymnasium.slug}), self.gymnasium_data)

        self.assertRedirects(r, '/gymnasium/watteau2/', fetch_redirect_response=False)
