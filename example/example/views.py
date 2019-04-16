# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging
from datetime import date

# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

# Current django project
from sports_manager.category.models import Category
from sports_manager.license.forms import LicenseCreationForm, LicenseCreationForm2
from sports_manager.license.models import License
from sports_manager.player.models import Player
from sports_manager.team.models import Team
from sports_manager.mixins import OwnerOrStaffMixin

logger = logging.getLogger(__name__)

class LicenseCreateAjaxGetCategories(View):

    http_method_names = ['get']
    template_name = 'sports_manager/license/ajax_get_categories.html'

    def calculate_age_player(self, player):
        today = date.today()
        age = today.year - player.birthday.year - \
            ((today.month, today.day) < (player.birthday.month, player.birthday.day))
        logger.debug("{} {} age: {}".format(player.first_name, player.last_name, age))
        return age
    
    def get_list_of_category(self, age):
        qs = Category.objects.all()
        qs = qs.filter(min_age__lte=age)
        logger.debug(qs)

        qs = qs.exclude(max_age__lte=age)
        logger.debug(qs)

        return qs

    def get(self, request, *args, **kwargs):
        player_id = request.GET.get('player')
        player = Player.objects.get(id=player_id)
        player_age = self.calculate_age_player(player)
        return render(request, self.template_name, {'categories': self.get_list_of_category(player_age)})


class LicenseCreateAjaxGetTeams(View):

    http_method_names = ['get']
    template_name = 'sports_manager/license/ajax_get_teams.html'
    
    def get_list_of_teams(self, category_id, sex):
        qs = Team.objects.all()
        qs = qs.filter(category__id=category_id).filter(sex__in=[sex, Team.SEXES[-1][0]])
        logger.debug(qs)

        return qs

    def get(self, request, *args, **kwargs):
        player_id = request.GET.get('player')
        category_id = request.GET.get('category')
        player = Player.objects.get(id=player_id)
        return render(request, self.template_name, {'teams': self.get_list_of_teams(category_id, player.sex)})