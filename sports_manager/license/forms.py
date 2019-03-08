# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django import forms

# Current django project
from sports_manager.license.models import License

logger = logging.getLogger(__name__)


class LicenseCreationForm(forms.ModelForm):
    """License creation form."""

    # player = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label=None)
    class Meta:
        model = License
        fields = [
            'player',
            'teams'
        ]
        widgets = {
            'teams': forms.CheckboxSelectMultiple
        }
