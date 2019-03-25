# -*- coding: utf-8 -*-
"""Player model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

# Current django project
from sports_manager.mixins import OwnerOrStaffMixin
from sports_manager.player.forms import EmergencyContactForm, MedicalCertificateForm, PlayerCreateForm, PlayerUpdateForm, StaffMedicalCertificateForm
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """View that returns the list of categories."""

    template_name = "sports_manager/player/list.html"
    model = Player

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(owner__username=self.kwargs.get('username'))


class PlayerDetailView(LoginRequiredMixin, OwnerOrStaffMixin, DetailView):
    """View that returns the details of a category."""

    template_name = "sports_manager/player/detail.html"
    model = Player

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(owner__username=self.kwargs.get('username'))


# class PlayerCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
#     """View that creates a Player."""

#     template_name = "sports_manager/player/create_form.html"
#     model = Player
#     form_class = PlayerCreateForm

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['username'] = self.request.user.get_username()
#         return kwargs

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.owner = self.request.user
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def get_success_url(self, **kwargs):
#         """Get the URL after the success."""
#         msg = _("Player '%(full_name)s' added successfully") % {'full_name': self.object.full_name}
#         messages.success(self.request, msg)
#         return self.object.get_absolute_url()


# class PlayerUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
#     """View that creates a Player."""

#     template_name = "sports_manager/player/update_form.html"
#     model = Player
#     form_class = PlayerUpdateForm

#     def get_success_url(self, **kwargs):
#         """Get the URL after the success."""
#         msg = _("Player '%(full_name)s' updated successfully") % {'full_name': self.object.full_name}
#         messages.success(self.request, msg)
#         return self.object.get_absolute_url()


class PlayerDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
    """View that deletes a new category."""

    template_name = "sports_manager/player/confirm_delete.html"
    model = Player

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Player '%(full_name)s' deleted successfully") % {'full_name': self.object.full_name}
        messages.success(self.request, msg)
        return reverse('sports-manager:player-list')


class PlayerCreateView(LoginRequiredMixin, OwnerOrStaffMixin, View):
    """Create a new user with multiple forms.

    Check http://www.joshuakehn.com/2013/7/18/multiple-django-forms-in-one-form.html.
    """

    template_name = 'sports_manager/player/create_form.html'
    player_form = PlayerCreateForm
    emergency_form = EmergencyContactForm
    certificate_form = MedicalCertificateForm

    def get(self, request, *args, **kwargs):
        """Return the three forms that are part of the creation view."""
        player_form = self.player_form(prefix="player", username=kwargs.get('username'))
        emergency_form = self.emergency_form(prefix="emergency")
        certificate_form = self.certificate_form(prefix="certif")
        return render(request,
                      self.template_name,
                      {
                          'player_form': player_form,
                          'emergency_form': emergency_form,
                          'certificate_form': certificate_form
                      })

    def post(self, request, *args, **kwargs):
        """Post data to the three forms that are part of the creation view."""
        player_form = self.player_form(request.POST, prefix="player", username=kwargs.get('username'))
        emergency_form = self.emergency_form(request.POST, prefix="emergency")
        certificate_form = self.certificate_form(request.POST, request.FILES, prefix="certif")

        if player_form.is_valid() and emergency_form.is_valid() and certificate_form.is_valid():
            self.player = player_form.save(commit=False)
            self.player.owner = get_user_model().objects.get(username=kwargs.get('username'))
            self.player.save()
            emergency_contact = emergency_form.save(commit=False)
            emergency_contact.player = self.player
            emergency_contact.save()
            medical_certificate = certificate_form.save(commit=False)
            if medical_certificate.file:
                medical_certificate.validation = MedicalCertificate.IN_VALIDATION
            else:
                medical_certificate.validation = MedicalCertificate.NOT_UPLOADED
            medical_certificate.player = self.player
            medical_certificate.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request,
                          self.template_name,
                          {
                              'player_form': player_form,
                              'emergency_form': emergency_form,
                              'certificate_form': certificate_form
                          })

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Player '%(name)s' created successfully") % {'name': self.player}
        messages.success(self.request, msg)
        return reverse('sports-manager:player-list', kwargs={'username': self.player.owner.get_username()})


class PlayerUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, View):
    """View that updates a new category."""

    template_name = "sports_manager/player/update_form.html"

    def get_objects(self, *args, **kwargs):
        player = Player.objects.get(owner__username=kwargs.get('username'), slug=kwargs.get('slug'))
        return {
            'player': player,
            'emergency_contact': player.emergencycontact_set.first(),
            'certificate': player.medicalcertificate_set.last()
        }
    
    def get_player_form(self, *args, **kwargs):
        if hasattr(self, 'player_form'):
            return self.player_form
        return PlayerUpdateForm
    
    def get_emergency_form(self, *args, **kwargs):
        if hasattr(self, 'emergency_form'):
            return self.emergency_form
        return EmergencyContactForm
    
    def get_certificate_form(self, user_is_staff=False):
        if hasattr(self, 'certificate_form'):
            return self.certificate_form
        return MedicalCertificateForm if not user_is_staff else StaffMedicalCertificateForm

    def get(self, request, *args, **kwargs):
        """Return the three forms that are part of the creation view."""
        logger.debug("Receive get")
        objs = self.get_objects(*args, **kwargs)
        player_form = self.get_player_form()(prefix="player", instance=objs['player'])
        emergency_form = self.get_emergency_form()(prefix="emergency", instance=objs['emergency_contact'])
        certificate_form = self.get_certificate_form(request.user.is_staff)(prefix="certif", instance=objs['certificate'])
        return render(request,
                      self.template_name,
                      {
                          'player': objs['player'],
                          'player_form': player_form,
                          'emergency_form': emergency_form,
                          'certificate_form': certificate_form
                      })

    def post(self, request, *args, **kwargs):
        """Post data to the three forms that are part of the creation view."""
        logger.debug("Receive post")
        objs = self.get_objects(*args, **kwargs)
        player_form = self.get_player_form()(request.POST, prefix="player", instance=objs['player'])
        emergency_form = self.get_emergency_form()(request.POST, prefix="emergency", instance=objs['emergency_contact'])
        certificate_form = self.get_certificate_form(request.user.is_staff)(request.POST, request.FILES, prefix="certif", instance=objs['certificate'])

        if player_form.is_valid() and emergency_form.is_valid() and certificate_form.is_valid():
            self.player = player_form.save(commit=False)
            self.player.owner = get_user_model().objects.get(username=kwargs.get('username'))
            self.player.save()
            emergency_contact = emergency_form.save(commit=False)
            emergency_contact.player = self.player
            emergency_contact.save()
            medical_certificate = certificate_form.save(commit=False)
            if medical_certificate.file:
                medical_certificate.validation = MedicalCertificate.IN_VALIDATION
            else:
                medical_certificate.validation = MedicalCertificate.NOT_UPLOADED
            medical_certificate.player = self.player
            medical_certificate.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            logger.error(certificate_form)
            return render(request,
                          self.template_name,
                          {
                              'player': objs['player'],
                              'player_form': player_form,
                              'emergency_form': emergency_form,
                              'certificate_form': certificate_form
                          })

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Player '%(name)s' updated successfully") % {'name': self.player.full_name}
        messages.success(self.request, msg)
        return self.player.get_absolute_url()