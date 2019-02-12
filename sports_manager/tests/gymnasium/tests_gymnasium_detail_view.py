#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.models import Gymnasium


class TestVcnAccountDetailViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.gymnasium = Gymnasium.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)
        self.gymnasium = Gymnasium.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsStaff(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        self.staff = get_user_model().objects.create_user(**self.dict)
        self.gymnasium = Gymnasium.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)


class TestVcnAccountDetailViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.dict)
        self.gymnasium = Gymnasium.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            surface=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)
