# -*- coding: utf-8 -*-
"""Team time slot model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.mixins import StaffMixin
from sports_manager.models import Team, TimeSlot

logger = logging.getLogger(__name__)


class TeamTimeSlotListView(StaffMixin, ListView):
    """View that returns the list of practices."""

    model = TimeSlot

    def get_context_data(self, **kwargs):
        """Add the team object got from the slug in the context data."""
        context = super().get_context_data(**kwargs)
        try:
            context['team'] = Team.objects.get(slug=self.kwargs['slug'])
        except Team.DoesNotExist as e:
            raise Http404("Team '{}'' does not exist".format(self.kwargs['slug']))
        if 'slug' in self.kwargs:
            context['team'] = Team.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        """Override get_queryset in order to retrieve time slots of one team only."""
        queryset = super().get_queryset()
        return queryset.filter(team__slug=self.kwargs['slug'])


class TeamTimeSlotDetailView(StaffMixin, DetailView):
    """View that returns the details of a Pratice."""

    model = TimeSlot

    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        try:
            context['team'] = Team.objects.get(slug=kwargs['slug'])
        except Team.DoesNotExist as e:
            raise Http404("Team '{}'' does not exist".format(kwargs['slug']))
        if 'slug' in kwargs:
            context['team'] = Team.objects.get(slug=kwargs['slug'])
        return context


class TeamTimeSlotCreateView(StaffMixin, CreateView):
    """View that creates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("TimeSlot '%(day)s' for '%(team)s' added successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'slug': self.object.team.slug})


class TeamTimeSlotUpdateView(StaffMixin, UpdateView):
    """View that updates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("TimeSlot '%(day)s' for '%(team)s' updated successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'slug': self.object.team.slug})


class TeamTimeSlotDeleteView(StaffMixin, DeleteView):
    """View that deletes a new TimeSlot."""

    model = TimeSlot

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("TimeSlot '%(day)s' for '%(team)s' deleted successfully") % {
            'day': self.object.day,
            'team': self.object.team.name
        }
        messages.success(self.request, msg)
        return reverse('sports-manager:team-detail', kwargs={'slug': self.object.team.slug})
