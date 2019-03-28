# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging
from datetime import date

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView

# Current django project
from sports_manager.category.models import Category
from sports_manager.license.forms import LicenseForm, StaffLicenseForm
from sports_manager.license.models import License
from sports_manager.mixins import OwnerOrStaffMixin
from sports_manager.player.models import Player
from sports_manager.team.models import Team

logger = logging.getLogger(__name__)


class LicenseListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """List of license."""

    template_name = "sports_manager/license/list.html"
    model = License
    paginate_by = 10

    def get_queryset(self):
        """Queryset."""
        queryset = super().get_queryset()
        return queryset.filter(player__owner__username=self.kwargs.get('username'))


class LicenseDetailView(LoginRequiredMixin, OwnerOrStaffMixin, DetailView):
    """Detail of a license."""

    template_name = "sports_manager/license/detail.html"
    model = License


class LicenseCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
    """Create a license for a logged user."""

    template_name = "sports_manager/license/create_form.html"
    model = License
    form_class = LicenseForm

    def form_valid(self, form):
        """Validate the form."""
        logger.debug("Form valid")
        self.object = form.save(commit=False)
        self.object.is_payed = False
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s created successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class LicenseUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
    """Update a license for a logged user."""

    template_name = "sports_manager/license/update_form.html"
    model = License
    form_class = LicenseForm

    def get_form_class(self):
        """Override the form class to get more fields if the user connected is a staff member."""
        if self.request.user.is_staff:
            self.form_class =  StaffLicenseForm
        return self.form_class

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s updated successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class LicenseDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
    """Delete a player's license."""

    template_name = "sports_manager/license/confirm_delete.html"
    model = License

    def get_queryset(self):
        """Return the list of license owned by the 'username'."""
        return super().get_queryset().filter(player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s updated successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()
