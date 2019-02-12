# -*- coding: utf-8 -*-
"""Team time slot model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.models import Team, TimeSlot

logger = logging.getLogger(__name__)


class TeamTimeSlotListView(ListView):
    """View that returns the list of practices."""

    model = TimeSlot


class TeamTimeSlotDetailView(DetailView):
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


class TeamTimeSlotCreateView(CreateView):
    """View that creates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "TimeSlot '{}' for '{}' added successfully".format(
            self.object.day, self.object.team.name))
        return reverse('sports-manager:time-slot-detail', kwargs={'pk': self.object.id})


class TeamTimeSlotUpdateView(UpdateView):
    """View that updates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "TimeSlot '{}' for '{}' updated successfully".format(
            self.object.day, self.object.team.name))
        return reverse('sports-manager:time-slot-detail', kwargs={'pk': self.object.pk})


class TeamTimeSlotDeleteView(DeleteView):
    """View that deletes a new TimeSlot."""

    model = TimeSlot

    def get(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_staff:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "TimeSlot '{}' for '{}' deleted successfully".format(
            self.object.day, self.object.team.name))
        return reverse('sports-manager:time-slot-list')
