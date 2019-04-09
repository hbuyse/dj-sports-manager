# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.models.season import Season
from sports_manager.mixins import StaffMixin

logger = logging.getLogger(__name__)


class SeasonListView(LoginRequiredMixin, StaffMixin, ListView):
    """List of Season."""

    template_name = "sports_manager/season/list.html"
    model = Season
    paginate_by = 10


class SeasonDetailView(LoginRequiredMixin, StaffMixin, DetailView):
    """Detail of a Season."""

    template_name = "sports_manager/season/detail.html"
    model = Season


class SeasonCreateView(LoginRequiredMixin, StaffMixin, CreateView):
    """Create a Season for a logged user."""

    template_name = "sports_manager/season/create_form.html"
    model = Season
    fields = [
        'start',
        'end'
    ]

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Season '%(str)s' created successfully") % {'str': str(self.object)}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class SeasonUpdateView(LoginRequiredMixin, StaffMixin, UpdateView):
    """Update a Season for a logged user."""

    template_name = "sports_manager/season/update_form.html"
    model = Season
    fields = [
        'start',
        'end'
    ]

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Season '%(str)s' updated successfully") % {'str': str(self.object)}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class SeasonDeleteView(LoginRequiredMixin, StaffMixin, DeleteView):
    """Delete a player's Season."""

    template_name = "sports_manager/season/confirm_delete.html"
    model = Season

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Season '%(str)s' deleted successfully") % {'str': str(self.object)}
        messages.success(self.request, msg)
        return reverse("sports-manager:season-list")
