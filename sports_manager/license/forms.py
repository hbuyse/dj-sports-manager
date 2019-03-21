# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django import forms

# Current django project
from sports_manager.license.models import License
from sports_manager.category.models import Category
from sports_manager.player.models import Player
from sports_manager.team.models import Team

logger = logging.getLogger(__name__)


class LicenseCreationForm(forms.ModelForm):
    """License creation form."""

    # player = forms.ModelChoiceField(queryset=Player.objects.none(), empty_label=None)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), empty_label=None)
    # teams = forms.ModelChoiceField(queryset=Team.objects.none(), widget=forms.CheckboxSelectMultiple, empty_label=None)

    class Meta:
        model = License
        fields = [
            'player',
            'category',
            'teams'
        ]
        widgets = {
            'teams': forms.CheckboxSelectMultiple
        }



class LicenseCreationForm2(forms.Form):
    """License creation form."""

    player = forms.ModelChoiceField(queryset=Player.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    teams = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple)

