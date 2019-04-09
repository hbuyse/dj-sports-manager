# -*- coding: utf-8

# Standard library
from datetime import date, timedelta

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

# Current django project
from sports_manager.forms.player import (
    EmergencyContactForm,
    MedicalCertificateForm,
    MedicalCertificateRenewForm,
    PlayerCreateForm,
    PlayerUpdateForm,
    StaffMedicalCertificateForm
)
# Local Django
from sports_manager.models.player import Player
from sports_manager.tests.helper import UserHelper


class TestPlayerCreateForm(TestCase):

    def test_empty(self):
        form_data = {}
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_birthday(self):
        form_data = {
            'birthday': date.today() - timedelta(weeks=20 * 52)
        }
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_names(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata"
        }
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_sex(self):
        form_data = {
            'sex': "MA"
        }
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_address(self):
        form_data = {
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=6)
    def test_invalid_with_min_age(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=(settings.SPORTS_MANAGER_PLAYER_MIN_AGE - 1) * 52),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings()
    def test_invalid_with_no_username(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data)
        # ValidationError: User None does not exist
        self.assertFalse(form.is_valid())

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=6)
    def test_valid_with_min_age(self):
        user = UserHelper()
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=settings.SPORTS_MANAGER_PLAYER_MIN_AGE * 52),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data, username=user.get('username'))
        self.assertTrue(form.is_valid())

    @override_settings()
    def test_valid_without_min_age(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        user = UserHelper()
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data, username=user.get('username'))
        self.assertTrue(form.is_valid())

    @override_settings()
    def test_valid_but_same_player_data_invalid(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        user = UserHelper()
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerCreateForm(data=form_data, username=user.get('username'))
        self.assertTrue(form.is_valid())
        obj = form.save(commit=False)
        obj.owner = user.object
        obj.save()
        form = PlayerCreateForm(data=form_data, username=user.get('username'))
        self.assertFalse(form.is_valid())


class TestPlayerUpdateForm(TestCase):

    def test_empty(self):
        form_data = {}
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_birthday(self):
        form_data = {
            'birthday': date.today() - timedelta(weeks=20 * 52)
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_names(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata"
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_sex(self):
        form_data = {
            'sex': "MA"
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_address(self):
        form_data = {
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=6)
    def test_invalid_with_min_age(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=(settings.SPORTS_MANAGER_PLAYER_MIN_AGE - 1) * 52),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @override_settings()
    def test_invalid_with_no_username(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=6)
    def test_valid_with_min_age(self):
        user = UserHelper()
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today() - timedelta(weeks=settings.SPORTS_MANAGER_PLAYER_MIN_AGE * 52),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings()
    def test_valid_without_min_age(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        user = UserHelper()
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'birthday': date.today(),
            'sex': "MA",
            'address': "Toto",
            'zip_code': "Toto",
            'city': "Toto",
        }
        form = PlayerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestEmergencyContact(TestCase):

    def test_empty(self):
        form_data = {}
        form = EmergencyContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_names(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata"
        }
        form = EmergencyContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_phone(self):
        form_data = {
            'phone': "0100000000"
        }
        form = EmergencyContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_only_email(self):
        form_data = {
            'email': "email@email.com"
        }
        form = EmergencyContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_without_email(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'phone': "0100000000"
        }
        form = EmergencyContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_with_email(self):
        form_data = {
            'first_name': "Toto",
            'last_name': "Tata",
            'phone': "0100000000",
            'email': "email@email.com"
        }
        form = EmergencyContactForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestMedicalCertificateForm(TestCase):

    def test_file_help_text_no_display(self):
        form = MedicalCertificateForm()
        self.assertEqual(len(form.fields['file'].help_text), 0)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf'])
    def test_file_help_text_ext_display(self):
        form = MedicalCertificateForm()
        self.assertIn("Extensions", form.fields['file'].help_text)
        self.assertIn(".pdf", form.fields['file'].help_text)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB=2)
    def test_file_help_text_size_display(self):
        form = MedicalCertificateForm()
        self.assertIn("Max size", form.fields['file'].help_text)
        self.assertIn("2 MB", form.fields['file'].help_text)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf'], SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB=2)
    def test_file_help_text_ext_and_size_display(self):
        form = MedicalCertificateForm()
        self.assertIn("Extensions", form.fields['file'].help_text)
        self.assertIn(".pdf", form.fields['file'].help_text)
        self.assertIn("Max size", form.fields['file'].help_text)
        self.assertIn("2 MB", form.fields['file'].help_text)


class TestStaffMedicalCertificateForm(TestCase):

    def test_file_help_text_no_display(self):
        form = StaffMedicalCertificateForm()
        self.assertEqual(len(form.fields['file'].help_text), 0)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf'])
    def test_file_help_text_ext_display(self):
        form = StaffMedicalCertificateForm()
        self.assertIn("Extensions", form.fields['file'].help_text)
        self.assertIn(".pdf", form.fields['file'].help_text)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB=2)
    def test_file_help_text_size_display(self):
        form = StaffMedicalCertificateForm()
        self.assertIn("Max size", form.fields['file'].help_text)
        self.assertIn("2 MB", form.fields['file'].help_text)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf'], SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB=2)
    def test_file_help_text_ext_and_size_display(self):
        form = StaffMedicalCertificateForm()
        self.assertIn("Extensions", form.fields['file'].help_text)
        self.assertIn(".pdf", form.fields['file'].help_text)
        self.assertIn("Max size", form.fields['file'].help_text)
        self.assertIn("2 MB", form.fields['file'].help_text)


class TestMedicalCertificateRenewForm(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = MedicalCertificateRenewForm

    def test_empty(self):
        form_data = {}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_not_valid_answer_id(self):
        form_data = {
            'answer': 3
        }
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_answer_id(self):
        for choice in MedicalCertificateRenewForm.CHOICES:
            form_data = {
                'answer': choice[0]
            }
            form = self.form(data=form_data)
            self.assertTrue(form.is_valid())

    def test_has_been_renewed_refused(self):
        form_data = {
            'answer': MedicalCertificateRenewForm.REFUSED
        }
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_been_renewed())

    def test_has_been_renewed_accepted(self):
        form_data = {
            'answer': MedicalCertificateRenewForm.ACCEPTED
        }
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.has_been_renewed())
