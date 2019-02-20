# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

# Current django project
from sports_manager.models.license import License
from sports_manager.forms.license import LicenseCreationForm

logger = logging.getLogger(__name__)


class LicenseListView(ListView):
    """List of license."""

    model = License
    paginate_by = 10

    def get_queryset(self):
        """Queryset."""
        return self.model.objects.filter(player__owner__username=self.kwargs.get('username'))

    def get(self, request, *args, **kwargs):
        """."""
        if request.user.is_anonymous:
            raise PermissionDenied
        elif kwargs['username'] != request.user.get_username() and not request.user.is_staff:
            raise PermissionDenied

        return super().get(request, args, kwargs)


class LicenseDetailView(DetailView):
    """Detail of a license."""

    model = License

    def get(self, request, *args, **kwargs):
        """View on a GET method."""
        self.object = self.get_object()

        if request.user.get_username() == self.object.player.owner.get_username():
            pass
        # If user is superuser or staff member
        elif request.user.is_staff:
            logger.info("{} {} accessed (GET) the URL {} owned by {}".format(
                "Superuser" if request.user.is_superuser else "Staff",
                request.user.get_username(),
                request.path,
                self.object.player.owner.username))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to GET the URL {} owned by {}".format(
                request.path, self.object.player.owner.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        else:
            logger.error("User {} tried to GET the URL {} owned by {}".format(
                request.user.get_username(), request.path, self.object.player.owner.username))
            raise PermissionDenied

        return super().get(request, *args, **kwargs)


class LicenseCreateView(CreateView):
    """Create a license for a logged user."""

    model = License
    form_class = LicenseCreationForm

    def post(self, request, *args, **kwargs):
        """Override post function."""
        if request.user.is_anonymous:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Validate the form."""
        form.instance.is_payed = False
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "License '{}' for '{}' created successfully".format(
            self.object.license_number, self.object.team.name))
        return reverse('sports-manager:license-detail', kwargs={'pk': self.object.pk})

        if request.user.get_username() == user.get_username():
            pass
        # If user is superuser or staff member
        elif request.user.is_staff:
            logger.info("{} {} accessed (POST) the URL {} owned by {}".format(
                "Superuser" if request.user.is_superuser else "Staff",
                request.user.get_username(),
                request.path,
                user.get_username()))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to POST the URL {} owned by {}".format(
                request.path, user.get_username()))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        else:
            logger.error("User {} tried to POST the URL {} owned by {}".format(
                request.user.get_username(), request.path, user.get_username()))
            raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """View on a GET method."""
        user = get_object_or_404(get_user_model(), *args, **kwargs)

        if request.user.get_username() == user.get_username():
            pass
        # If user is superuser or staff member
        elif request.user.is_staff:
            logger.info("{} {} accessed (GET) the URL {} owned by {}".format(
                "Superuser" if request.user.is_superuser else "Staff",
                request.user.get_username(),
                request.path,
                user.get_username()))
            pass
        # Anonymous user can not update account
        elif request.user.is_anonymous:
            logger.error("Anonymous user tried to GET the URL {} owned by {}".format(
                request.path, user.get_username()))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        else:
            logger.error("User {} tried to GET the URL {} owned by {}".format(
                request.user.get_username(), request.path, user.get_username()))
            raise PermissionDenied

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Validate the form."""
        form.instance.is_payed = False

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "License for {} {} created successfully".format(
            self.object.player, self.object.teams))
        logger.debug(kwargs)
        return reverse('sports-manager:license-detail', kwargs={'username': self.object.player.owner.get_username(), 'pk': self.object.pk})
