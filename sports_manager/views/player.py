# -*- coding: utf-8 -*-
"""Player model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.forms.player import EmergencyContactForm, MedicalCertificateForm, PlayerCreationForm
from sports_manager.mixins import OwnerOrStaffMixin
from sports_manager.models import Player

logger = logging.getLogger(__name__)


class PlayerListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """View that returns the list of categories."""

    model = Player

    def get_queryset(self):
        """Override the getter of the queryset.
        
        This view will ony show the player owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(owner__username=self.kwargs.get('username'))


class PlayerDetailView(LoginRequiredMixin, OwnerOrStaffMixin, DetailView):
    """View that returns the details of a category."""

    model = Player

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner__username=self.kwargs.get('username'))


class PlayerCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
    """View that creates a new category."""

    model = Player
    form_class = PlayerCreationForm

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Player '{}' added successfully".format(self.object.name))
        return reverse('sports-manager:player-detail', kwargs={'slug': self.object.slug})


class PlayerUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
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
        return reverse('sports-manager:player-detail', kwargs={'slug': self.object.slug})


class PlayerDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
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
        return reverse('sports-manager:player-list')


def create_new_player(request, username):
    """Check http://www.joshuakehn.com/2013/7/18/multiple-django-forms-in-one-form.html."""
    if request.POST:
        logger.debug("Receive post")
        player_form = PlayerCreationForm(request.POST, prefix="player")
        emergency_form = EmergencyContactForm(request.POST, prefix="emergency")
        certificate_form = MedicalCertificateForm(request.POST, request.FILES, prefix="certif")
    
        if player_form.is_valid() and emergency_form.is_valid() and certificate_form.is_valid():
            player = player_form.save(commit=False)
            player.owner = request.user
            player.save()
            emergency_contact = emergency_form.save(commit=False)
            emergency_contact.player = player
            emergency_contact.save()
            medical_certificate = certificate_form.save(commit=False)
            medical_certificate.player = player
            medical_certificate.save()

            return HttpResponseRedirect(reverse('sports-manager:player-list', kwargs={'username': request.user.get_username()}))
    else:
        player_form = PlayerCreationForm(prefix="player")
        emergency_form = EmergencyContactForm(prefix="emergency")
        certificate_form = MedicalCertificateForm(prefix="certif")

    return render(request,
                  'sports_manager/player_creation_form.html',
                  {'player_form': player_form, 'emergency_form': emergency_form, 'certificate_form': certificate_form}
    )