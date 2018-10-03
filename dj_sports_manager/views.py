# -*- coding: utf-8 -*-
"""Models."""

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
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
    TimeSlot,
    License,
)

from .views_category import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
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
    fields = '__all__'
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


class TeamTimeSlotListView(ListView):
    """View that returns the list of practices."""

    model = TimeSlot


class TeamTimeSlotDetailView(DetailView):
    """View that returns the details of a Pratice."""

    model = TimeSlot

    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        try:
            context['team'] = Team.objects.get(slug=kwargs['slug'])
        except Team.DoesNotExist:
            raise Http404("Team '{}'' does not exist".format(kwargs['slug']))
        if 'slug' in kwargs:
            context['team'] = Team.objects.get(slug=kwargs['slug'])
        return context


class TeamTimeSlotCreateView(CreateView):
    """View that creates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

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

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "TimeSlot '{}' for '{}' added successfully".format(
            self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:time-slot-detail', kwargs={'pk': self.object.id})


class TeamTimeSlotUpdateView(UpdateView):
    """View that updates a new TimeSlot."""

    model = TimeSlot
    fields = '__all__'

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

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "TimeSlot '{}' for '{}' updated successfully".format(
            self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:time-slot-detail', kwargs={'pk': self.object.pk})


class TeamTimeSlotDeleteView(DeleteView):
    """View that deletes a new TimeSlot."""

    model = TimeSlot

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
        messages.success(self.request, "TimeSlot '{}' for '{}' deleted successfully".format(
            self.object.day, self.object.team.name))
        return reverse('dj-sports-manager:time-slots-list')


class LicenseListView(ListView):
    """List of license."""

    model = License

    def get(self, request, *args, **kwargs):
        """."""
        if request.user.is_anonymous:
            raise PermissionDenied

        return super().get(request, args, kwargs)


class LicenseDetailView(DetailView):
    """Detail of a license."""

    model = License

    def get(self, request, *args, **kwargs):
        """View on a GET method."""
        self.object = self.get_object()

        if request.user.id == self.object.id:
            pass
        # If user is superuser or staff member
        elif request.user.is_staff:
            logger.info("{} {} accessed (GET) the URL {} owned by {}".format(
                "Superuser" if request.user.is_superuser else "Staff",
                request.user.username,
                request.path,
                self.object.owner.username))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to GET the URL {} owned by {}".format(
                request.path, self.object.owner.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        else:
            logger.error("User {} tried to GET the URL {} owned by {}".format(
                request.user.username, request.path, self.object.owner.username))
            raise PermissionDenied

        return super().get(request, *args, **kwargs)


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
        messages.success(self.request, "License '{}' for '{}' created successfully".format(
            self.object.license_number, self.object.team.name))
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
        messages.success(self.request, "License '{}' for '{}' created successfully".format(
            self.object.license_number, self.object.team.name))
        return reverse('dj-sports-manager:license-update', kwargs={'pk': self.object.pk})


class LicenseDeleteView(DeleteView):
    """Delete a license for a logged user."""

    model = License

    def get(self, request, *args, **kwargs):
        """View on a GET method."""
        # If user is superuser
        if request.user.is_superuser:
            logger.info("Superuser {} accessed (GET) the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # If user is part of staff
        elif request.user.is_staff:
            logger.info("Staff user {} accessed (GET) the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to GET the DeleteView of {}'s account.".format(self.object.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        elif request.user.id != self.object.id:
            logger.error("User {} tried to GET the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        # If user is superuser
        if request.user.is_superuser:
            logger.info("Superuser {} accessed (GET) the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # If user is part of staff
        elif request.user.is_staff:
            logger.info("Staff user {} accessed (GET) the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to GET the DeleteView of {}'s account.".format(self.object.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        elif request.user.id != self.object.id:
            logger.error("User {} tried to GET the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "License '{}' for '{}' deleted successfully".format(
            self.object.license_number, self.object.team.name))
        return reverse('dj-sports-manager:licenses-list')
