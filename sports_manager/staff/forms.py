# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _  # noqa

from markdownx.fields import MarkdownxFormField

# Current django project
from sports_manager.team.models import Team

logger = logging.getLogger(__name__)


class StaffSendEmailForm(forms.Form):
    """Staff sending email form."""

    teams = forms.ModelChoiceField(queryset=Team.objects.all(),
                                   empty_label=None,
                                   required=True,
                                   help_text="Select the teams you want to send a email to",
                                   widget=forms.CheckboxSelectMultiple
                                   )
    subject = forms.CharField(max_length=256, required=True)
    text = MarkdownxFormField(required=True)
    files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}),
                            required=False)

    def get_list_of_recipients(self):
        logger.debug(self.cleaned_data['teams'])

    def send_email(self):
        pass
