#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sports-manager` models module."""

# Standard library
from datetime import date, timedelta
from unittest import mock

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase, override_settings

# Current django project
from sports_manager.player.validators import is_player_old_enough, validate_file_extension, validate_file_size


class TestIsPlayerOldEnough(TestCase):

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_not_old_enough(self):
        for i in range(0, settings.SPORTS_MANAGER_PLAYER_MIN_AGE):
            birthday = date.today() - timedelta(weeks=i*52)
            with self.assertRaises(ValidationError):
                is_player_old_enough(birthday)

    @override_settings(SPORTS_MANAGER_PLAYER_MIN_AGE=7)
    def test_old_enough(self):
        for i in range(7, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)

    @override_settings()
    def test_no_min_age_given(self):
        del settings.SPORTS_MANAGER_PLAYER_MIN_AGE
        for i in range(0, 100):
            birthday = date.today() - timedelta(weeks=i*52)
            is_player_old_enough(birthday)


class TestValidateFileExtension(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ext_list = ['.pdf', '.doc', '.docx']

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf'])
    def test_list_one(self):
        for i in self.ext_list:
            file_mock = mock.MagicMock(spec=File)
            file_mock.name = 'test{}'.format(i)
            if i in settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST:
                validate_file_extension(file_mock)
            else:
                with self.assertRaises(ValidationError):
                    validate_file_extension(file_mock)

    @override_settings(SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST=['.pdf', '.doc', '.docx'])
    def test_list_multiple(self):
        for i in self.ext_list:
            file_mock = mock.MagicMock(spec=File)
            file_mock.name = 'test{}'.format(i)
            validate_file_extension(file_mock)

    @override_settings()
    def test_list_empty(self):
        del settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST
        for i in self.ext_list:
            file_mock = mock.MagicMock(spec=File)
            file_mock.name = 'test{}'.format(i)
            validate_file_extension(file_mock)


class TestValidateFileSize(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.size_list = [2, 2 << 10, 2 << 20, 2 << 200 + 1]
        pass

    @override_settings(SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB=2)
    def test_list_one(self):
        for i in self.size_list:
            file_mock = mock.MagicMock(spec=File)
            file_mock.size = i
            if i <= (settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB << 20) :
                validate_file_size(file_mock)
            else:
                with self.assertRaises(ValidationError):
                    validate_file_size(file_mock)

    @override_settings()
    def test_list_empty(self):
        del settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB
        for i in self.size_list:
            file_mock = mock.MagicMock(spec=File)
            file_mock.size = i
            validate_file_size(file_mock)
