# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging
from datetime import date, timedelta

# Django
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, DateInput, Form, ModelChoiceField, ModelForm, ModelMultipleChoiceField

# Current django project
from sports_manager.models import Player

logger = logging.getLogger(__name__)


class PlayerCreationForm(ModelForm):
    
        model = Player
        widgets = {
            "birthday": DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        }
        fields = ['first_name', 'last_name', 'birthday', 'sex']
