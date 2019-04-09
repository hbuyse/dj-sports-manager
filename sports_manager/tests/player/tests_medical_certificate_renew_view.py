#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase, override_settings
from django.urls import reverse

# Current django project
from sports_manager.forms.player import MedicalCertificateRenewForm
from sports_manager.models.player import MedicalCertificate
from sports_manager.tests.helper import MedicalCertificateHelper, PlayerHelper, UserHelper


class TestMedicalCertificateRenewViewAsAnonymous(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='user')
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        if 'wrong_account' in test_name:
            self.certif = MedicalCertificateHelper(player=self.other_player)
            self.certif.create()
            if 'in_validation' in test_name:
                pass
            elif 'valid' in test_name:
                self.certif.validation = MedicalCertificate.VALID
                self.certif.update()

    def test_get_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             dict(self.certif.datas_for_form))
        self.assertEqual(r.status_code, 403)


class TestMedicalCertificateRenewViewAsLogged(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper()
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        self.certif = MedicalCertificateHelper(
            player=self.other_player if 'wrong_account' in test_name else self.player)
        self.certif.create()
        if 'in_validation' in test_name:
            pass
        elif 'valid' in test_name:
            self.certif.validation = MedicalCertificate.VALID
            self.certif.update()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 403)

    def test_get_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('object', r.context)
        self.assertEqual(r.context['object'], self.certif._object)

    def test_post_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 403)

    def test_post_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertRedirects(r, self.certif._object.get_absolute_url(), fetch_redirect_response=False)
        self.certif.refresh_from_db()
        self.assertEqual(self.certif.get('renewals'), 1)


class TestMedicalCertificateRenewViewAsStaff(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper(is_staff=True)
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        self.certif = MedicalCertificateHelper(
            player=self.other_player if 'wrong_account' in test_name else self.player)
        self.certif.create()
        if 'in_validation' in test_name:
            pass
        elif 'valid' in test_name:
            self.certif.validation = MedicalCertificate.VALID
            self.certif.update()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('object', r.context)
        self.assertEqual(r.context['object'], self.certif._object)

    def test_get_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('object', r.context)
        self.assertEqual(r.context['object'], self.certif._object)

    def test_post_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertRedirects(r, self.certif._object.get_absolute_url(), fetch_redirect_response=False)
        self.certif.refresh_from_db()
        self.assertEqual(self.certif.get('renewals'), 1)

    def test_post_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertRedirects(r, self.certif._object.get_absolute_url(), fetch_redirect_response=False)
        self.certif.refresh_from_db()
        self.assertEqual(self.certif.get('renewals'), 1)


class TestMedicalCertificateRenewViewAsSuperuser(TestCase):
    """Tests UpdateView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.other = UserHelper(username='other')
        cls.user = UserHelper(is_superuser=True)
        cls.other_player = PlayerHelper(owner=cls.other)
        cls.other_player.create()
        cls.player = PlayerHelper(owner=cls.user)
        cls.player.create()

    def setUp(self):
        test_name = self.id().split('.')[-1]
        self.certif = MedicalCertificateHelper(
            player=self.other_player if 'wrong_account' in test_name else self.player)
        self.certif.create()
        if 'in_validation' in test_name:
            pass
        elif 'valid' in test_name:
            self.certif.validation = MedicalCertificate.VALID
            self.certif.update()
        self.assertTrue(self.client.login(**(dict(self.user.get_credentials()))))

    def test_get_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('object', r.context)
        self.assertEqual(r.context['object'], self.certif._object)

    def test_get_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 404)

    def test_get_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.get(reverse('sports-manager:player-medical-certificate-renew',
                                    kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('object', r.context)
        self.assertEqual(r.context['object'], self.certif._object)

    def test_post_wrong_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_wrong_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.other.get_username(), 'player': self.other_player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertRedirects(r, self.certif._object.get_absolute_url(), fetch_redirect_response=False)
        self.certif.refresh_from_db()
        self.assertEqual(self.certif.get('renewals'), 1)

    def test_post_right_account_player_not_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_not_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug') + 'a', 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_no_certificate(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk + 1}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_in_validation(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertEqual(r.status_code, 404)

    def test_post_right_account_player_existing_one_certificate_valid(self):
        """Tests."""
        r = self.client.post(reverse('sports-manager:player-medical-certificate-renew',
                                     kwargs={'username': self.user.get_username(), 'player': self.player.get('slug'), 'pk': self.certif.pk}),
                             {'answer': MedicalCertificateRenewForm.ACCEPTED})
        self.assertRedirects(r, self.certif._object.get_absolute_url(), fetch_redirect_response=False)
        self.certif.refresh_from_db()
        self.assertEqual(self.certif.get('renewals'), 1)