# -*- coding: utf-8 -*-
"""Team model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.mixins import StaffMixin
from sports_manager.team.models import Team, TimeSlot

logger = logging.getLogger(__name__)


class TeamListView(ListView):
    """View that returns the list of categories."""

    template_name = "sports_manager/team/list.html"
    model = Team


class TeamDetailView(DetailView):
    """View that returns the details of a team."""

    template_name = "sports_manager/team/detail.html"
    model = Team
    slug_url_kwarg = 'team'


class TeamCreateView(LoginRequiredMixin, StaffMixin, CreateView):
    """View that creates a new team."""

    template_name = "sports_manager/team/create_form.html"
    model = Team
    fields = [
        'name',
        'category',
        'level',
        'sex',
        'recruitment',
        'url',
        'description',
        'img',
    ]

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Team '%(name)s' created successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'team': self.object.slug})


class TeamUpdateView(LoginRequiredMixin, StaffMixin, UpdateView):
    """View that updates a new team."""

    template_name = "sports_manager/team/update_form.html"
    model = Team
    slug_url_kwarg = 'team'
    fields = [
        'name',
        'category',
        'level',
        'sex',
        'recruitment',
        'url',
        'description',
        'img',
    ]

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Team '%(name)s' updated successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'team': self.object.slug})


class TeamDeleteView(LoginRequiredMixin, StaffMixin, DeleteView):
    """View that deletes a new team."""

    template_name = "sports_manager/team/confirm_delete.html"
    model = Team
    slug_url_kwarg = 'team'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Team '%(name)s' deleted successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:team-list')


class TeamTimeSlotListView(StaffMixin, ListView):
    """View that returns the list of practices."""

    template_name = "sports_manager/timeslot/list.html"
    model = TimeSlot

    def get_queryset(self):
        """Override get_queryset in order to retrieve time slots of one team only."""
        queryset = super().get_queryset()
        return queryset.filter(team__slug=self.kwargs['team'])


class TeamTimeSlotDetailView(StaffMixin, DetailView):
    """View that returns the details of a Pratice."""

    template_name = "sports_manager/timeslot/detail.html"
    model = TimeSlot

    def get_queryset(self):
        """Override get_queryset in order to retrieve time slots of one team only."""
        queryset = super().get_queryset()
        return queryset.filter(team__slug=self.kwargs['team'])


class TeamTimeSlotCreateView(StaffMixin, CreateView):
    """View that creates a new TimeSlot."""

    template_name = "sports_manager/timeslot/create_form.html"
    model = TimeSlot
    fields = [
        'type',
        'gymnasium',
        'day',
        'start',
        'end'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = get_object_or_404(Team, slug=self.kwargs['team'])  # Check that the team we want to edit exist
        return context

    def form_valid(self, form):
        """Override the form_valid method to set the team for which we create the timeslot."""
        self.object = form.save(commit=False)
        self.object.team = Team.objects.get(slug=self.kwargs.get('team'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Timeslot of '%(day)s' for '%(team)s' added successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'team': self.object.team.slug})


class TeamTimeSlotUpdateView(StaffMixin, UpdateView):
    """View that updates a new TimeSlot."""

    template_name = "sports_manager/timeslot/update_form.html"
    model = TimeSlot
    fields = [
        'type',
        'gymnasium',
        'day',
        'start',
        'end'
    ]

    def get_queryset(self):
        """Override get_queryset in order to retrieve time slots of one team only."""
        queryset = super().get_queryset()
        return queryset.filter(team__slug=self.kwargs['team'])

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Timeslot of '%(day)s' for '%(team)s' updated successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'team': self.object.team.slug})


class TeamTimeSlotDeleteView(StaffMixin, DeleteView):
    """View that deletes a new TimeSlot."""

    template_name = "sports_manager/timeslot/confirm_delete.html"
    model = TimeSlot

    def get_queryset(self):
        """Override get_queryset in order to retrieve time slots of one team only."""
        queryset = super().get_queryset()
        return queryset.filter(team__slug=self.kwargs['team'])

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Timeslot of '%(day)s' for '%(team)s' deleted successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'team': self.object.team.slug})
