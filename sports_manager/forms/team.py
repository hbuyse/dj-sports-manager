# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging
from datetime import date, timedelta

# Django
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, DateInput, Form, ModelChoiceField, ModelForm, ModelMultipleChoiceField

# Current django project
from sports_manager.models.team import TimeSlot

logger = logging.getLogger(__name__)


class TimeSlotForm(ModelForm):
    
    class Meta:
        model = Player
        widgets = {
            "birthday": DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        }
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'sex'
        ]
