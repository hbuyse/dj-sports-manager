# -*- coding: utf-8 -*-
"""Player model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.forms.player import PlayerCreationForm
from sports_manager.models import Player

logger = logging.getLogger(__name__)


def test_user_staff(request):
    """Test if the connected user is part of staff."""
    return request.user.is_staff


def test_user_superuser(request):
    """Test if the connected user is a superuser."""
    return request.user.is_superuser


def test_user_own_page(request, kwargs, field_to_test):
    """Test if the user logged in owned the page asked to be accessed."""
    return request.user.username == kwargs.get(field_to_test) 


def test_access_private_page(request, kwargs, field_to_test):
    """Fusion of all the tests defined above."""
    return test_user_staff(request) or \
            test_user_superuser(request) or \
            test_user_own_page(request, kwargs, field_to_test)


class PlayerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View that returns the list of categories."""

    model = Player
    permission_denied_message = "You do not have the right to view this page."            # from AccessMixin
    raise_exception = True

    def test_func(self):
        return test_access_private_page(self.request, self.kwargs, 'username')

    def get_queryset(self):
        """Override the getter of the queryset.
        
        This view will ony show the player owned by the <username> user.
        """
        return self.model.objects.filter(owner__username=self.kwargs.get('username'))


class PlayerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View that returns the details of a category."""

    model = Player
    permission_denied_message = "You do not have the right to view this page."            # from AccessMixin
    raise_exception = True

    def test_func(self):
        return test_access_private_page(self.request, self.kwargs, 'username')


class PlayerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View that creates a new category."""

    model = Player
    form_class = PlayerCreationForm
    permission_denied_message = "You do not have the right to view this page."            # from AccessMixin
    raise_exception = True

    def test_func(self):
        return test_access_private_page(self.request, self.kwargs, 'username')

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Player '{}' added successfully".format(self.object.name))
        return reverse('sports-manager:category-detail', kwargs={'slug': self.object.slug})


class PlayerUpdateView(UpdateView):
    """View that updates a new category."""

    model = Player
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Player '{}' updated successfully".format(self.object.name))
        return reverse('sports-manager:category-detail', kwargs={'slug': self.object.slug})


class PlayerDeleteView(DeleteView):
    """View that deletes a new category."""

    model = Player

    def get(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied

        return super().post(request, args, kwargs)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "Player '{}' deleted successfully".format(self.object.name))
        return reverse('sports-manager:categorie-list')
