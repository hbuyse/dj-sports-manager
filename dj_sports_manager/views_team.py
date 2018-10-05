# -*- coding: utf-8 -*-
"""Team model views."""

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Team,
)

logger = logging.getLogger(__name__)


class TeamListView(ListView):
    """View that returns the list of categories."""

    model = Team


class TeamDetailView(DetailView):
    """View that returns the details of a team."""

    model = Team
    slug_field = 'slug'


class TeamCreateView(CreateView):
    """View that creates a new team."""

    model = Team
    fields = [
        'name',
        'category',
        'level',
        'sex',
        'is_recruiting',
        'url',
        'description',
        'img',
    ]

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

    def form_valid(self, form):
        """Override form validation for slug field."""
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Team '{}' added successfully".format(self.object.name))
        return reverse('dj-sports-manager:team-detail', kwargs={'slug': self.object.slug})


class TeamUpdateView(UpdateView):
    """View that updates a new team."""

    model = Team
    slug_field = 'slug'
    fields = [
        'name',
        'category',
        'level',
        'sex',
        'is_recruiting',
        'url',
        'description',
        'img',
    ]

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

    def form_valid(self, form):
        """Override form validation for slug field."""
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Team '{}' updated successfully".format(self.object.name))
        return reverse('dj-sports-manager:team-detail', kwargs={'slug': self.object.slug})


class TeamDeleteView(DeleteView):
    """View that deletes a new team."""

    model = Team
    slug_field = 'slug'

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
        messages.success(self.request, "Team '{}' deleted successfully".format(self.object.name))
        return reverse('dj-sports-manager:teams-list')
