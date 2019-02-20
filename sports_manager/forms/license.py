# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

# Current django project
from sports_manager.models.license import License
from sports_manager.models.team import Team

logger = logging.getLogger(__name__)


class LicenseCreationForm(ModelForm):
    
    teams = ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=CheckboxSelectMultiple,
        label=_("Select the teams")
    )

    class Meta:
        model = License
        fields = [
            'player'
        ]
