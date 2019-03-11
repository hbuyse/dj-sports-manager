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
from sports_manager.player.models import (
    EmergencyContact,
    MedicalCertificate,
    Player,
    file_upload_to
)
from sports_manager.team.models import Team
from sports_manager.tests.helper import create_user


class TestPlayerModel(TestCase):

    def test_string_representation(self):
        p = Player(first_name="Toto", last_name="Tata")
        self.assertEqual(str(p), "Toto Tata")

    def test_verbose_name(self):
        self.assertEqual(str(Player._meta.verbose_name), "player")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Player._meta.verbose_name_plural), "players")

    def test_save(self):
        user = create_user()[1]
        p = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user)
        self.assertEqual(len(p.slug), 0)
        p.save()
        self.assertEqual(p.slug, "toto-tata")
    
    def test_get_absolute_url(self):
        user = create_user()[1]
        p = Player(first_name="Toto", last_name="Tata", birthday=date.today() - timedelta(weeks=7*52), owner=user)
        p.save()
        self.assertEqual(p.get_absolute_url(), "/{}/player/toto-tata/".format(user.get_username()))


class TestMedicalCertificate(TestCase):

    def test_string_representation(self):
        p = Player(first_name="Toto", last_name="Tata")
        m = MedicalCertificate(player=p)
        self.assertEqual(str(m), "Toto Tata (not uploaded - start: {})".format(m.start))

    def test_verbose_name(self):
        self.assertEqual(str(MedicalCertificate._meta.verbose_name), "medical certificate")

    def test_verbose_name_plural(self):
        self.assertEqual(str(MedicalCertificate._meta.verbose_name_plural), "medical certificates")
    
    def test_is_valid(self):
        p = Player(first_name="Toto", last_name="Tata")
        tests = (
            (MedicalCertificate.NOT_UPLOADED, False),
            (MedicalCertificate.IN_VALIDATION, False),
            (MedicalCertificate.VALID, True),
            (MedicalCertificate.REJECTED, False)
        )
        for test in tests:
            m = MedicalCertificate(player=p, validation=test[0])
            self.assertEqual(m.is_valid(), test[1])


class TestEmergencyContact(TestCase):

    def test_string_representation(self):
        p = Player(first_name="Toto", last_name="Tata")
        e = EmergencyContact(first_name="Titi", last_name="Tutu", player=p)
        self.assertEqual(str(e), "Titi Tutu (Toto Tata)")

    def test_verbose_name(self):
        self.assertEqual(str(EmergencyContact._meta.verbose_name), "emergency contact")

    def test_verbose_name_plural(self):
        self.assertEqual(str(EmergencyContact._meta.verbose_name_plural), "emergency contacts")
