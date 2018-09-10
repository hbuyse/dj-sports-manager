# -*- coding: utf-8 -*-
"""Models."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Category,
    Team,
    Practice,
    License,
)


class CategoryListView(ListView):
    """View that returns the list of categories."""

    model = Category


class CategoryDetailView(DetailView):
    """View that returns the details of a category."""

    model = Category
    slug_field = 'name'


class CategoryCreateView(CreateView):
    """View that creates a new category."""

    model = Category
    fields = '__all__'

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
        messages.success(self.request, "Category '{}' added successfully".format(self.object.name))
        return reverse('dj-sports-manager:category-detail', kwargs={'pk': self.object.id})


class CategoryUpdateView(UpdateView):
    """View that updates a new category."""

    model = Category
    fields = '__all__'

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
        messages.success(self.request, "Category '{}' updated successfully".format(self.object.name))
        return reverse('dj-sports-manager:category-detail', kwargs={'pk': self.object.id})


class CategoryDeleteView(DeleteView):
    """View that deletes a new category."""

    model = Category

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
        messages.success(self.request, "Category '{}' deleted successfully".format(self.object.name))
        return reverse('dj-sports-manager:categories-list')


class TeamListView(ListView):
    """View that returns the list of categories."""

    model = Team


class TeamDetailView(DetailView):
    """View that returns the details of a team."""

    model = Team


class TeamCreateView(CreateView):
    """View that creates a new team."""

    model = Team
    fields = '__all__'

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
        messages.success(self.request, "Team '{}' added successfully".format(self.object.name))
        return reverse('dj-sports-manager:team-detail', kwargs={'pk': self.object.id})


class TeamUpdateView(UpdateView):
    """View that updates a new team."""

    model = Team
    fields = '__all__'

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
        messages.success(self.request, "Team '{}' updated successfully".format(self.object.name))
        return reverse('dj-sports-manager:team-detail', kwargs={'pk': self.object.id})


class TeamDeleteView(DeleteView):
    """View that deletes a new team."""

    model = Category

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
        messages.success(self.request, "Team '{}' deleted successfully".format(self.object.name))
        return reverse('dj-sports-manager:teams-list')


class PracticeListView(ListView):
    """View that returns the list of practices."""

    model = Practice


class PracticeDetailView(DetailView):
    """View that returns the details of a Pratice."""

    model = Practice


class PracticeCreateView(CreateView):
    """View that creates a new Practice."""

    model = Practice
    fields = '__all__'

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
        messages.success(self.request, "Practice '{}' for '{}' added successfully".format(self.object.day, self.object.teams.name))
        return reverse('dj-sports-manager:practice-detail', kwargs={'pk': self.object.id})


class PracticeUpdateView(UpdateView):
    """View that updates a new Practice."""

    model = Practice
    fields = '__all__'

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
        messages.success(self.request, "Practice '{}' for '{}' updated successfully".format(self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:practice-detail', kwargs={'pk': self.object.id})


class PracticeDeleteView(DeleteView):
    """View that deletes a new Practice."""

    model = Practice

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
        messages.success(self.request, "Practice '{}' for '{}' deleted successfully".format(self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:practices-list')


class LicenseCreateView(CreateView):

    model = License


class LicenseDeleteView(DeleteView):

    model = License


class LicenseDetailView(DetailView):

    model = License


class LicenseUpdateView(UpdateView):

    model = License


class LicenseListView(ListView):

    model = License
