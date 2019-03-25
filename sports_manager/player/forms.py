# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import DateInput, ModelForm
from django.utils.translation import ugettext_lazy as _  # noqa

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerCreateForm(ModelForm):
    """Player form.
    
    This first form will check if there is already a Player with the same datas linked to the user."""

    class Meta:
        model = Player
        widgets = {
            "birthday": DateInput(attrs={'class': 'form-control'})
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

        if Player.objects.filter(**datas).exists:
            raise ValidationError(_("A player with the first name (%(first_name)s) and last name (%(last_name)s) "
                                    "already exists for user '%(username)s'."),
                                  params={
                                      'username': datas['owner__username'],
                                      'first_name': datas['first_name'],
                                      'last_name': datas['last_name'],
                                  })

        # Always return cleaned_data
        return cleaned_data


class PlayerUpdateForm(ModelForm):
    """Player update form.
    
    This first form will not check if there is already a Player with the same datas linked to the user."""

    class Meta:
        model = Player
        widgets = {
            "birthday": DateInput(attrs={'class': 'form-control'})
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
        ]
        localized_fields = ('birthday',)


class EmergencyContactForm(ModelForm):
    """Emergency contact form."""

    class Meta:
        model = EmergencyContact
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
        ]


class MedicalCertificateForm(ModelForm):
    """Medical certificate form."""

    class Meta:
        model = MedicalCertificate
        fields = [
            'file',
        ]
        help_texts = {
            'file': 'Extensions: {}. Max size: {} MB.'.format(', '.join(settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST), settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB),
        }



class StaffMedicalCertificateForm(ModelForm):
    """Medical certificate form."""

    class Meta:
        model = MedicalCertificate
        fields = [
            'file',
            'validation',
            'start',
            'end'
        ]
        help_texts = {
            'file': 'Extensions: {}. Max size: {} MB.'.format(', '.join(settings.SPORTS_MANAGER_CERTIFICATE_VALID_EXT_LIST), settings.SPORTS_MANAGER_CERTIFICATE_MAX_SIZE_MB),
        }
