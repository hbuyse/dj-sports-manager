# -*- coding: utf-8

# Standard library
from datetime import date, timedelta

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

# Current django project
# Local Django
from sports_manager.player.forms import EmergencyContactForm, MedicalCertificateForm, PlayerCreationForm
from sports_manager.tests.helper import create_user


class TestBreakfastForm(TestCase):
    """Form to alternate participants between two breakfasts."""

    def test_empty(self):
        form_data = {}
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_birthday(self):
        form_data = {
            'birthday': date.today() - timedelta(weeks=20 * 52)
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_names(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata"
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_sex(self):
        form_data = {
            'sex': "MA"
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings(SPORT_MANAGER_PLAYER_MIN_AGE=6)
    def test_invalid_with_min_age(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=(settings.SPORT_MANAGER_PLAYER_MIN_AGE - 1) * 52),
            'sex': "MA"
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings(SPORT_MANAGER_PLAYER_MIN_AGE=6)
    def test_valid_with_min_age(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=settings.SPORT_MANAGER_PLAYER_MIN_AGE * 52),
            'sex': "MA"
        }
        form = PlayerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings()
    def test_valid_without_min_age(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA"
        }
        form = PlayerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
