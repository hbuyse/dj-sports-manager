# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _

# Current django project
from sports_manager.models.license import License
from sports_manager.models.player import Player
from sports_manager.models.team import Team

logger = logging.getLogger(__name__)


class LicenseCreationForm(forms.ModelForm):

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
