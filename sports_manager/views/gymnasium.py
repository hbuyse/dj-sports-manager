# coding=utf-8

"""Views."""

# Django
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.models import Gymnasium


class GymnasiumListView(ListView):
    """View that returns the list of Gymnasiums."""

    model = Gymnasium
    paginate_by = 10


class GymnasiumDetailView(DetailView):
    """Show the details of a Gymnasium."""

    model = Gymnasium
    slug_field = 'slug'


class GymnasiumCreateView(CreateView):
    """Create a Gymnasium."""

    model = Gymnasium
    fields = [
        'name',
        'address',
        'city',
        'zip_code',
        'phone',
        'surface',
        'capacity',
    ]

    def get(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Gymnasium '{}' added successfully".format(self.object.name))
        return reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.object.slug})


class GymnasiumUpdateView(UpdateView):
    """Update a Gymnasium."""

    model = Gymnasium
    slug_field = 'slug'
    fields = [
        'name',
        'address',
        'city',
        'zip_code',
        'phone',
        'surface',
        'capacity',
    ]

    def get(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:

            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Gymnasium '{}' updated successfully".format(self.object.name))
        return reverse('sports-manager:gymnasium-detail', kwargs={'slug': self.object.slug})


class GymnasiumDeleteView(DeleteView):
    """Delete of a Gymnasium."""

    model = Gymnasium
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "Gymnasium '{}' deleted successfully".format(self.object.name))
        return reverse('sports-manager:gymnasium-list')
