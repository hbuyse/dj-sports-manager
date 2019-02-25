# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.forms.license import LicenseCreationForm
from sports_manager.mixins import OwnerOrStaffMixin
from sports_manager.models.license import License

logger = logging.getLogger(__name__)


class LicenseListView(OwnerOrStaffMixin, ListView):
    """List of license."""

    model = License
    paginate_by = 10

    def get_queryset(self):
        """Queryset."""
        queryset = super().get_queryset()
        return queryset.filter(player__owner__username=self.kwargs.get('username'))


class LicenseDetailView(OwnerOrStaffMixin, DetailView):
    """Detail of a license."""

    model = License


class LicenseCreateView(CreateView):
    """Create a license for a logged user."""

    model = License
    form_class = LicenseCreationForm
    # fields = ['player', 'teams']

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s created successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.is_payed = False
        self.object.save()
        print(form.is_valid())
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class LicenseUpdateView(UpdateView):
    """Create a license for a logged user."""

    model = License
    form_class = LicenseCreationForm

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s updated successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.save()
        print(form.cleaned_data)
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())
