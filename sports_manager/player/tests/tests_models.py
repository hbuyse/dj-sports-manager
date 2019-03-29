#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Standard library
from datetime import date, timedelta

# Django
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player, file_upload_to
from sports_manager.tests.helper import UserHelper


class TestFileUploadTo(TestCase):
    """Test the path creation function."""

    def test_with_no_category_object(self):
        t = 0
        self.assertEqual(file_upload_to(t, 'Toto.pdf'), None)

    def test_with_category_object(self):
        user = UserHelper()
        player = Player(first_name='Titi', last_name='Tutu', owner=user.object)
        med_cert = MedicalCertificate(player=player)
        self.assertEqual(file_upload_to(med_cert, 'Toto.pdf'), '{}/titi_tutu/{}/medical_certificate.pdf'.format(user.get_username(), date.today().year))


class TestPlayerModel(TestCase):

    def test_string_representation(self):
        p = Player(first_name="Toto", last_name="Tata")
        self.assertEqual(str(p), "Toto Tata")

    def test_verbose_name(self):
        self.assertEqual(str(Player._meta.verbose_name), "player")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Player._meta.verbose_name_plural), "players")

    def test_save(self):
        user = UserHelper()
        p = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user.object)
        self.assertEqual(len(p.slug), 0)
        p.save()
        self.assertEqual(p.slug, "toto-tata")

    def test_full_name(self):
        user = UserHelper()
        p = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user.object)
        self.assertEqual(p.full_name, "Toto Tata")

    def test_get_absolute_url(self):
        user = UserHelper()
        p = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user.object)
        p.save()
        self.assertEqual(p.get_absolute_url(), "/{}/player/toto-tata/".format(user.get_username()))


class TestMedicalCertificate(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserHelper()
        cls.player = Player.objects.create(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=cls.user.object)

    def test_string_representation(self):
        m = MedicalCertificate(player=self.player)
        self.assertEqual(str(m), "Toto Tata (not uploaded - start: {})".format(m.start))

    def test_verbose_name(self):
        self.assertEqual(str(MedicalCertificate._meta.verbose_name), "medical certificate")

    def test_verbose_name_plural(self):
        self.assertEqual(str(MedicalCertificate._meta.verbose_name_plural), "medical certificates")

    def test_is_valid(self):
        tests = (
            (MedicalCertificate.NOT_UPLOADED, False),
            (MedicalCertificate.IN_VALIDATION, False),
            (MedicalCertificate.VALID, True),
            (MedicalCertificate.REJECTED, False)
        )
        for test in tests:
            m = MedicalCertificate(player=self.player, validation=test[0])
            self.assertEqual(m.is_valid(), test[1])

    def test_save(self):
        m = MedicalCertificate(player=self.player)
        self.assertIsNone(m.start)
        m.save()
        self.assertEqual(m.start, date.today())

    def test_get_absolute_url(self):
        """Test the get_absolute_url from the model MedicalCertificate."""
        m = MedicalCertificate(player=self.player)
        m.save()
        self.assertEqual(m.get_absolute_url(), '/{}/player/{}/medical-certificate/{}/'.format(m.player.owner.get_username(), m.player.slug, m.pk))


class TestEmergencyContact(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserHelper()
        cls.player = Player.objects.create(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=cls.user.object)

    def test_string_representation(self):
        p = Player(first_name="Toto", last_name="Tata")
        e = EmergencyContact(first_name="Titi", last_name="Tutu", player=p)
        self.assertEqual(str(e), "Titi Tutu (Toto Tata)")

    def test_verbose_name(self):
        self.assertEqual(str(EmergencyContact._meta.verbose_name), "emergency contact")

    def test_verbose_name_plural(self):
        self.assertEqual(str(EmergencyContact._meta.verbose_name_plural), "emergency contacts")

    def test_get_absolute_url(self):
        """Test the get_absolute_url from the model MedicalCertificate."""
        m = MedicalCertificate(player=self.player)
        m.save()
        self.assertEqual(m.get_absolute_url(), '/{}/player/{}/medical-certificate/{}/'.format(m.player.owner.get_username(), m.player.slug, m.pk))
