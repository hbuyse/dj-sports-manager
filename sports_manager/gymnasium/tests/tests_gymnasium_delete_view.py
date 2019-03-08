#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Current django project
from sports_manager.gymnasium.models import Gymnasium


class TestVcnAccountDeleteViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.gymnasium = Gymnasium.objects.create(
            name='Watteau',
            address='37 rue Lequesne',
            city='Nogent-Sur-Marne',
            zip_code=94130,
            phone='0100000000',
            area=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 403)


class TestVcnAccountDeleteViewAsLogged(TestCase):
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
            area=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))
        self.assertEqual(r.status_code, 403)


class TestVcnAccountDeleteViewAsStaff(TestCase):
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
            area=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))

        self.assertRedirects(r, '/gymnasium/', fetch_redirect_response=False)


class TestVcnAccountDeleteViewAsSuperuser(TestCase):
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
            area=123,
            capacity=456
        )
        self.gymnasium.save()

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))

        self.assertEqual(r.status_code, 200)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('sports-manager:gymnasium-delete', kwargs={'slug': self.gymnasium.slug}))

        self.assertRedirects(r, '/gymnasium/', fetch_redirect_response=False)
