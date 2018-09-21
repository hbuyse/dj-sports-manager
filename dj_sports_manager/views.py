# -*- coding: utf-8 -*-
"""Models."""

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
    Category,
    Team,
    TimeSlot,
    License,
)


logger = logging.getLogger(__name__)


class CategoryListView(ListView):
    """View that returns the list of categories."""

    model = Category


class CategoryDetailView(DetailView):
    """View that returns the details of a category."""

    model = Category
    slug_field = 'slug'


class CategoryCreateView(CreateView):
    """View that creates a new category."""

    model = Category
    fields = [
        'name',
        'min_age',
        'max_age',
        'summary',
        'description',
        'img',
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

    def form_valid(self, form):
        """Override form validation for slug field."""
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Category '{}' added successfully".format(self.object.name))
        return reverse('dj-sports-manager:category-detail', kwargs={'slug': self.object.slug})


class CategoryUpdateView(UpdateView):
    """View that updates a new category."""

    model = Category
    slug_field = 'slug'
    fields = [
        'name',
        'min_age',
        'max_age',
        'summary',
        'description',
        'img',
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

    def form_valid(self, form):
        """Override form validation for slug field."""
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Category '{}' updated successfully".format(self.object.name))
        return reverse('dj-sports-manager:category-detail', kwargs={'slug': self.object.slug})


class CategoryDeleteView(DeleteView):
    """View that deletes a new category."""

    model = Category
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
        messages.success(self.request, "Category '{}' deleted successfully".format(self.object.name))
        return reverse('dj-sports-manager:categories-list')


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
        if True not in [request.user.is_superuser, request.user.is_staff]:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if True not in [request.user.is_superuser, request.user.is_staff]:
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
    fields = '__all__'
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


class TeamPracticeListView(ListView):
    """View that returns the list of practices."""

    model = TimeSlot


class TeamPracticeDetailView(DetailView):
    """View that returns the details of a Pratice."""

    model = TimeSlot


class TeamPracticeCreateView(CreateView):
    """View that creates a new TimeSlot."""

    model = TimeSlot
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
        messages.success(self.request, "TimeSlot '{}' for '{}' added successfully".format(self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:practice-detail', kwargs={'pk': self.object.id})


class TeamPracticeUpdateView(UpdateView):
    """View that updates a new TimeSlot."""

    model = TimeSlot
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
        messages.success(self.request, "TimeSlot '{}' for '{}' updated successfully".format(self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:practice-detail', kwargs={'pk': self.object.pk})


class TeamPracticeDeleteView(DeleteView):
    """View that deletes a new TimeSlot."""

    model = TimeSlot

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
        messages.success(self.request, "TimeSlot '{}' for '{}' deleted successfully".format(self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:practices-list')


class LicenseListView(ListView):
    """List of license."""

    model = License


class LicenseDetailView(DetailView):
    """Detail of a license."""

    model = License


class LicenseCreateView(CreateView):
    """Create a license for a logged user."""

    model = License
    fields = [
        'first_name',
        'last_name',
        'sex',
        'birthday',
        'team',
    ]

    def post(self, request, *args, **kwargs):
        """Override post function."""
        if request.user.is_anonymous:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Validate the form."""
        form.instance.owner = self.request.user
        form.instance.is_payed = False
        form.instance.is_captain = False

        if form.instance.certif:
            form.instance.certif_valid = License.CERTIFICATION_IN_VALIDATION
        else:
            form.instance.certif_valid = License.CERTIFICATION_NOT_UPLOADED

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "License '{}' for '{}' created successfully".format(self.object.license_number, self.object.team.name))
        return reverse('dj-sports-manager:license-detail', kwargs={'pk': self.object.pk})


class LicenseUpdateView(UpdateView):
    """Update a license for a logged user."""

    model = License
    fields = [
        'first_name',
        'last_name',
        'sex',
        'birthday',
        'team',
    ]

    def get(self, request, *args, **kwargs):
        """."""
        if request.user.is_anonymous:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if request.user.is_anonymous:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "License '{}' for '{}' created successfully".format(self.object.license_number, self.object.team.name))
        return reverse('dj-sports-manager:license-update', kwargs={'pk': self.object.pk})


class LicenseDeleteView(DeleteView):
    """Delete a license for a logged user."""

    model = License

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
        messages.success(self.request, "License '{}' for '{}' deleted successfully".format(self.object.license_number, self.object.team.name))
        return reverse('dj-sports-manager:practices-list')
