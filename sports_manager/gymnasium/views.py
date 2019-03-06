# coding=utf-8

"""Views."""

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.mixins import LoginRequiredMixin, StaffMixin
from sports_manager.gymnasium.models import Gymnasium


class GymnasiumListView(ListView):
    """View that returns the list of Gymnasiums."""

    template_name = "sports_manager/gymnasium/list.html"
    model = Gymnasium
    paginate_by = 10


class GymnasiumDetailView(DetailView):
    """Show the details of a Gymnasium."""

    template_name = "sports_manager/gymnasium/detail.html"
    model = Gymnasium
    slug_field = 'slug'


class GymnasiumCreateView(LoginRequiredMixin, StaffMixin, CreateView):
    """Create a Gymnasium."""

    template_name = "sports_manager/gymnasium/form.html"
    model = Gymnasium
    fields = [
        'type',
        'name',
        'address',
        'city',
        'zip_code',
        'phone',
        'area',
        'capacity',
    ]

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Gymnasium '%(name)s' added successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.object.slug})


class GymnasiumUpdateView(LoginRequiredMixin, StaffMixin, UpdateView):
    """Update a Gymnasium."""

    template_name = "sports_manager/gymnasium/form.html"
    model = Gymnasium
    slug_field = 'slug'
    fields = [
        'type',
        'name',
        'address',
        'city',
        'zip_code',
        'phone',
        'area',
        'capacity',
    ]

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Gymnasium '%(name)s' updated successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.object.slug})


class GymnasiumDeleteView(LoginRequiredMixin, StaffMixin, DeleteView):
    """Delete of a Gymnasium."""

    template_name = "sports_manager/gymnasium/confirm_delete.html"
    model = Gymnasium
    slug_field = 'slug'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Gymnasium '%(name)s' deleted successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:gymnasium-list')
