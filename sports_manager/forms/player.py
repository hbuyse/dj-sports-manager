# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _  # noqa

# Current django project
from sports_manager.models.player import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerCreateForm(forms.ModelForm):
    """Player form.

    This first form will check if there is already a Player with the same datas linked to the user.
    """

    class Meta:
        model = Player
        widgets = {
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "identity_card": forms.FileInput(),
            "identity_photo": forms.FileInput()
        }
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'sex',
            'address',
            'add_address',
            'zip_code',
            'city',
            'phone',
            'email',
            'identity_card',
            'identity_photo',
        ]
        localized_fields = ('birthday',)

    def __init__(self, *args, **kwargs):
        """Override init in order to get the owner of the page."""
        self.username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        datas = {
            'owner__username': self.username,
            'first_name': cleaned_data.get('first_name'),
            'last_name': cleaned_data.get('last_name'),
        }

        if not get_user_model().objects.filter(username=self.username).exists():
            raise ValidationError(_("User (%(username)s) does not exist."), params={'username': self.username})
        elif Player.objects.filter(**datas).exists():
            raise ValidationError(_("A player with the first name (%(first_name)s) and last name (%(last_name)s) "
                                    "already exists for user '%(username)s'."),
                                  params={
                                      'username': datas['owner__username'],
                                      'first_name': datas['first_name'],
                                      'last_name': datas['last_name'],
            })

        # Always return cleaned_data
        return cleaned_data


class PlayerUpdateForm(forms.ModelForm):
    """Player update form.

    This first form will not check if there is already a Player with the same datas linked to the user.
    """

    class Meta:
        model = Player
        widgets = {
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "identity_card": forms.FileInput(),
            "identity_photo": forms.FileInput()
        }
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'sex',
            'address',
            'add_address',
            'zip_code',
            'city',
            'phone',
            'email',
            'identity_card',
            'identity_photo',
        ]
        localized_fields = ('birthday',)


class EmergencyContactForm(forms.ModelForm):
    """Emergency contact form."""

    class Meta:
        model = EmergencyContact
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
        ]


class MedicalCertificateForm(forms.ModelForm):
    """Medical certificate form."""

    class Meta:
        model = MedicalCertificate
        fields = [
            'file',
        ]
        widgets = {
            "file": forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(settings, 'SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST'):
            self.fields['file'].help_text += 'Extensions: {}. '.format(
                ', '.join(settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST))

        if hasattr(settings, 'SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB'):
            self.fields['file'].help_text += 'Max size: {} MB. '.format(
                settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB)


class StaffMedicalCertificateForm(MedicalCertificateForm):
    """Medical certificate form."""

    class Meta(MedicalCertificateForm.Meta):
        model = MedicalCertificate
        fields = [
            'file',
            'validation',
            'start',
            'end'
        ]

class MedicalCertificateRenewForm(forms.Form):
    """Renewable medical certificate form."""

    REFUSED = 0
    ACCEPTED = 1

    CHOICES = (
        (REFUSED, _('no')),
        (ACCEPTED, _('yes'))
    )

    answer = forms.ChoiceField(choices=CHOICES, initial=REFUSED, widget=forms.RadioSelect)

    def has_been_renewed(self):
        """User accepted the renewable terms."""
        return int(self.cleaned_data["answer"]) == self.ACCEPTED
