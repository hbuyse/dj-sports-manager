# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging
from datetime import date, timedelta

# Django
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, DateInput, Form, ModelChoiceField, ModelForm, ModelMultipleChoiceField

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerCreationForm(ModelForm):
    
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
    
    class Meta:
        model = EmergencyContact
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
        ]


class MedicalCertificateForm(ModelForm):
    
    class Meta:
        model = MedicalCertificate
        fields = [
            'file',
        ]
