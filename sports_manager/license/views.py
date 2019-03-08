# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

# Current django project
from sports_manager.license.forms import LicenseCreationForm
from sports_manager.license.models import License
from sports_manager.mixins import OwnerOrStaffMixin

logger = logging.getLogger(__name__)


class LicenseListView(OwnerOrStaffMixin, ListView):
    """List of license."""

    template_name = "sports_manager/license/list.html"
    model = License
    paginate_by = 10

    def get_queryset(self):
        """Queryset."""
        queryset = super().get_queryset()
        return queryset.filter(player__owner__username=self.kwargs.get('username'))


class LicenseDetailView(OwnerOrStaffMixin, DetailView):
    """Detail of a license."""

    template_name = "sports_manager/license/detail.html"
    model = License


class LicenseCreateView(CreateView):
    """Create a license for a logged user."""

    template_name = "sports_manager/license/form.html"
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
    """Update a license for a logged user."""

    template_name = "sports_manager/license/form.html"
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


class LicenseDeleteView(DeleteView):
    """Delete a player's license."""

    template_name = "sports_manager/license/confirm_delete.html"
    model = License

    def get_queryset(self):
        """Return the list of license owned by the 'username'."""
        return super().get_queryset.filter(player__owner__username=self.kwargs.get('username'))

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
