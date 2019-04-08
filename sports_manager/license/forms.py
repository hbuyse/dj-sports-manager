# -*- coding: utf-8 -*-
"""Player forms."""

# Standard library
import logging
from datetime import date, datetime

# Django
from django import forms
from django.utils.translation import ugettext_lazy as _  # noqa

# Current django project
from sports_manager.category.models import Category
from sports_manager.license.models import License
from sports_manager.player.models import Player

logger = logging.getLogger(__name__)


class LicenseForm(forms.ModelForm):
    """License creation form."""

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    # upgraded = forms.BooleanField(required=False, initial=False)

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
        help_texts = {
            'player': "Select one of your players.",
            'category': "The category you want your player to evolve in."
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.filter(owner=user)

    def calculate_age(self, birthday):
        """Calculate the age from the birthday to today."""
        today = date.today() 
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day)) 
        return age
    
    def get_datetime_start_last_season(self):
        today = date.today() 
        if today.month <= 7:
            return datetime(today.year - 1, 7, 1)
        else:
            return datetime(today.year, 7, 1)

    def check_player_is_in_category_ages(self, category, player):
        player_age = self.calculate_age(player.birthday)
        if category.max_age:
            if not category.min_age <= player_age < category.max_age:
                self.add_error('category',
                    _("For the category '%(category)s', a player should be between %(min_age)d and %(max_age)d years old"
                    " (%(full_name)s is %(player_age)d)") % {
                        'category': category.name,
                        'min_age': category.min_age,
                        'max_age': category.max_age,
                        'full_name': player.full_name,
                        'player_age': player_age,
                    })
        else:
            if not category.min_age <= player_age:
                self.add_error('category',
                    _("For the category '%(category)s', a player should be at least %(min_age)d years old"
                    " (%(full_name)s is %(player_age)d)") % {
                        'category': category.name,
                        'min_age': category.min_age,
                        'full_name': player.full_name,
                        'player_age': player_age,
                    })

    def check_teams_are_in_category(self, teams, category):
        # Check that the team if part of the category
        for team in teams:
            if category != team.category:
                self.add_error('teams', _("The category '%(category)s' does not contain the team %(team)s") % {
                        'category': category.name,
                        'team': str(team),
                    })

    def check_player_already_has_license_in_category(self, player, category):
        qs = player.license_set.filter(created__gte=self.get_datetime_start_last_season(), teams__category=category)
        if qs.exists():
            logger.error("Player {} already has a license in the category {}.".format(player.full_name, category.name))
            raise forms.ValidationError(
                _("Player %(full_name)s already has a license in the category %(category)s for this season."
                  "You have to find and edit the license."),
                params={
                    'full_name': player.full_name,
                    'category': category.name,
                })

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data.get('player')
        category = cleaned_data.get('category')
        teams = cleaned_data.get('teams')

        # Check relations category - player
        self.check_player_is_in_category_ages(category, player)
        self.check_player_already_has_license_in_category(player, category)

        # Check relations category - teams
        self.check_teams_are_in_category(teams, category)


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
