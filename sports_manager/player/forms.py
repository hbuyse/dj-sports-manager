# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.forms import DateInput, ModelForm

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerCreationForm(ModelForm):
    """Player creation form."""

    class Meta:
        model = Player
        widgets = {
            "birthday": DateInput(attrs={'class': 'form-control'})
        }
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'sex'
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
