# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django import forms

# Current django project
from sports_manager.license.models import License

logger = logging.getLogger(__name__)


class LicenseForm(forms.ModelForm):
    """License creation form."""

    class Meta:
        model = License
        fields = [
            'player',
            'teams'
        ]
        widgets = {
            'teams': forms.CheckboxSelectMultiple
        }


class StaffLicenseForm(forms.ModelForm):
    """License creation form."""

    class Meta:
        model = License
        fields = [
            'player',
            'teams',
            'number',
            'is_payed'
        ]
        widgets = {
            'teams': forms.CheckboxSelectMultiple
        }
