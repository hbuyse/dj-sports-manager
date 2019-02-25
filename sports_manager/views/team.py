# -*- coding: utf-8 -*-
"""Team model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.models import Team
from sports_manager.mixins import StaffMixin

logger = logging.getLogger(__name__)


class TeamListView(ListView):
    """View that returns the list of categories."""

    model = Team


class TeamDetailView(DetailView):
    """View that returns the details of a team."""

    model = Team
    slug_field = 'slug'


class TeamCreateView(StaffMixin, CreateView):
    """View that creates a new team."""

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
        return reverse('sports-manager:team-detail', kwargs={'slug': self.object.slug})


class TeamUpdateView(StaffMixin, UpdateView):
    """View that updates a new team."""

    model = Team
    slug_field = 'slug'
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
        return reverse('sports-manager:team-detail', kwargs={'slug': self.object.slug})


class TeamDeleteView(StaffMixin, DeleteView):
    """View that deletes a new team."""

    model = Team
    slug_field = 'slug'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Team '%(name)s' deleted successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:team-list')
