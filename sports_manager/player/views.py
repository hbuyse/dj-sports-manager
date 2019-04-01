# -*- coding: utf-8 -*-
"""Player model views."""

# Standard library
import logging

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

# Current django project
from sports_manager.mixins import OwnerOrStaffMixin
from sports_manager.player.forms import (
    EmergencyContactForm,
    MedicalCertificateForm,
    MedicalCertificateRenewForm,
    PlayerCreateForm,
    PlayerUpdateForm,
    StaffMedicalCertificateForm
)
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

logger = logging.getLogger(__name__)


class PlayerListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """View that returns the list of categories."""

    template_name = "sports_manager/player/list.html"
    model = Player

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["owner"] = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return context

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


class PlayerCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
    """View that creates a Player."""

    template_name = "sports_manager/player/create_form.html"
    model = Player
    form_class = PlayerCreateForm

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["owner"] = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['username'] = self.kwargs.get('username')
        return kwargs

    def form_valid(self, form):
        """Override to make some changes before saving the object."""
        self.object = form.save(commit=False)
        self.object.owner = get_user_model().objects.get(username=self.kwargs.get('username'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Player '%(full_name)s' added successfully") % {'full_name': self.object.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class PlayerUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
    """View that creates a Player."""

    template_name = "sports_manager/player/update_form.html"
    model = Player
    form_class = PlayerUpdateForm

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs.get('slug'), owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Player '%(full_name)s' updated successfully") % {'full_name': self.object.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class PlayerDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
    """View that deletes a new category."""

    template_name = "sports_manager/player/confirm_delete.html"
    model = Player

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs.get('slug'), owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Player '%(full_name)s' deleted successfully") % {'full_name': self.object.full_name}
        messages.success(self.request, msg)
        return reverse('sports-manager:player-list', kwargs={'username': self.object.owner.get_username()})


class EmergencyContactListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """View that returns the list of categories."""

    template_name = "sports_manager/emergency_contact/list.html"
    model = EmergencyContact

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["player"] = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        return context

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))


class EmergencyContactDetailView(LoginRequiredMixin, OwnerOrStaffMixin, DetailView):
    """View that returns the details of a category."""

    template_name = "sports_manager/emergency_contact/detail.html"
    model = EmergencyContact

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))


class EmergencyContactCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
    """View that creates a EmergencyContact."""

    template_name = "sports_manager/emergency_contact/create_form.html"
    model = EmergencyContact
    form_class = EmergencyContactForm

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["player"] = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        return context

    def form_valid(self, form):
        """Override to make some changes before saving the object."""
        self.object = form.save(commit=False)
        self.object.player = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Emergency contact of player '%(full_name)s' added successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class EmergencyContactUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
    """View that creates a EmergencyContact."""

    template_name = "sports_manager/emergency_contact/update_form.html"
    model = EmergencyContact
    form_class = EmergencyContactForm

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Emergency contact of player '%(full_name)s' updated successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class EmergencyContactDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
    """View that creates a EmergencyContact."""

    template_name = "sports_manager/emergency_contact/confirm_delete.html"
    model = EmergencyContact

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Emergency contact of player '%(full_name)s' deleted successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return reverse("sports-manager:player-emergency-contact-list",
                       kwargs={"username": self.object.player.owner.get_username(), "player": self.object.player.slug}
                       )


class MedicalCertificateListView(LoginRequiredMixin, OwnerOrStaffMixin, ListView):
    """View that returns the list of categories."""

    template_name = "sports_manager/medical_certificate/list.html"
    model = MedicalCertificate

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["player"] = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        return context

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))


class MedicalCertificateDetailView(LoginRequiredMixin, OwnerOrStaffMixin, DetailView):
    """View that returns the details of a category."""

    template_name = "sports_manager/medical_certificate/detail.html"
    model = MedicalCertificate

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))


class MedicalCertificateCreateView(LoginRequiredMixin, OwnerOrStaffMixin, CreateView):
    """View that creates a MedicalCertificate."""

    template_name = "sports_manager/medical_certificate/create_form.html"
    model = MedicalCertificate
    form_class = MedicalCertificateForm

    def get_context_data(self, **kwargs):
        """Add the player in the context of the ListView."""
        context = super().get_context_data(**kwargs)
        context["player"] = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        return context

    def form_valid(self, form):
        """Override to make some changes before saving the object."""
        self.object = form.save(commit=False)
        self.object.player = get_object_or_404(
            Player, owner__username=self.kwargs.get('username'), slug=self.kwargs.get('player'))
        if self.object.file:
            self.object.validation = MedicalCertificate.IN_VALIDATION
        else:
            self.object.validation = MedicalCertificate.NOT_UPLOADED
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Medical certificate of player '%(full_name)s' added successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class MedicalCertificateUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, UpdateView):
    """View that creates a MedicalCertificate."""

    template_name = "sports_manager/medical_certificate/update_form.html"
    model = MedicalCertificate
    form_class = MedicalCertificateForm

    def get_form_class(self):
        """Return the form class to use."""
        if self.request.user.is_staff:
            return StaffMedicalCertificateForm
        return self.form_class

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Medical certificate of player '%(full_name)s' updated successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class MedicalCertificateDeleteView(LoginRequiredMixin, OwnerOrStaffMixin, DeleteView):
    """View that creates a MedicalCertificate."""

    template_name = "sports_manager/medical_certificate/confirm_delete.html"
    model = MedicalCertificate

    def get_queryset(self):
        """Override the getter of the queryset.

        This method will only get the players owned by the <username> user.
        """
        queryset = super().get_queryset()
        return queryset.filter(
            player__slug=self.kwargs.get('player'), player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Medical certificate of player '%(full_name)s' deleted successfully") % {
            'full_name': self.object.player.full_name}
        messages.success(self.request, msg)
        return reverse("sports-manager:player-medical-certificate-list",
                       kwargs={"username": self.object.player.owner.get_username(), "player": self.object.player.slug}
                       )


class MedicalCertificateRenewView(LoginRequiredMixin, OwnerOrStaffMixin, SingleObjectMixin, FormView):
    """Allow the user to renew a MedicalCertificate already saved."""

    template_name = "sports_manager/medical_certificate/renew_form.html"
    model = MedicalCertificate
    context_object_name = "medicalcertificate"
    form_class = MedicalCertificateRenewForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        """Override get_queryset in order to retrieve a correct list of MedicalCertificate that can be renewed."""
        queryset = super().get_queryset()
        queryset = queryset.filter(player__slug=self.kwargs.get('player'),
                                   player__owner__username=self.kwargs.get('username'),
                                   validation=self.model.VALID,
                                   renewals__lt=settings.SPORTS_MANAGER_MEDICAL_CERTIFICATE_MAX_RENEW)
        return queryset
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})
        
        self.object = obj
        return obj

    def form_valid(self, form):
        """Increase the number of renewals of a MedicalCertificate."""
        if form.has_been_renewed():
            self.object = self.get_object(self.get_queryset())
            self.object.renewals += 1
            self.object.save()
            msg = _("Medical certificate of player '%(name)s' renewed successfully") % {
                'name': self.object.player.full_name}
            messages.success(self.request, msg)
            logger.info("User '{}' has renewed the medical certificate of player '{}' for another year.".format(
                self.request.user.get_username(), self.object.player)
            )
        else:
            msg = _("Medical certificate of player '%(name)s' has not been renewed.") % {
                'name': self.object.player.full_name}
            messages.warning(self.request, msg)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        return self.object.get_absolute_url()


class PlayerAllInOneCreateView(LoginRequiredMixin, OwnerOrStaffMixin, View):
    """Create a new user with multiple forms.

    Check http://www.joshuakehn.com/2013/7/18/multiple-django-forms-in-one-form.html.
    """

    template_name = 'sports_manager/player/create_aio_form.html'
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


class PlayerAllInOneUpdateView(LoginRequiredMixin, OwnerOrStaffMixin, View):
    """View that updates a new category."""

    template_name = "sports_manager/player/update_aio_form.html"

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
        certificate_form = self.get_certificate_form(request.user.is_staff)(
            prefix="certif", instance=objs['certificate'])
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
        emergency_form = self.get_emergency_form()(request.POST, prefix="emergency",
                                                   instance=objs['emergency_contact'])
        certificate_form = self.get_certificate_form(request.user.is_staff)(
            request.POST, request.FILES, prefix="certif", instance=objs['certificate'])

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
