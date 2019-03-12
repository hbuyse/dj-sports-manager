# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging

# Django
from django.core.exceptions import ValidationError
from django.forms import DateInput, ModelForm
from django.utils.translation import ugettext_lazy as _  # noqa

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

    def __init__(self, *args, **kwargs):
        """Override init in order to get the owner of the page."""
        self.username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Check if there is a player that already exists.

        We check the first name, last name and birthday for a given owner.
        """
        d = {
            'owner__username': self.username,
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('last_name'),
            'birthday': self.cleaned_data.get('birthday')
        }
        logger.debug(d)
        if Player.objects.filter(**d).exists():
            raise ValidationError(
                _("Player '%(first_name)s %(last_name)s' of owner '%(username)s' already exists.") % {
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'username': d['owner__username'],
                })
        return self.cleaned_data


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
