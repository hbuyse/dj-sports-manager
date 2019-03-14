# -*- coding: utf-8 -*-
"""Models."""

# Standard library
import logging
from datetime import date

# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

# Current django project
from sports_manager.category.models import Category
from sports_manager.license.forms import LicenseCreationForm, LicenseCreationForm2
from sports_manager.license.models import License
from sports_manager.player.models import Player
from sports_manager.team.models import Team
from sports_manager.mixins import OwnerOrStaffMixin

logger = logging.getLogger(__name__)


class LicenseListView(OwnerOrStaffMixin, ListView):
    """List of license."""

    template_name = "sports_manager/license/list.html"
    model = License
    paginate_by = 10

    def get_queryset(self):
        """Queryset."""
        queryset = super().get_queryset()
        return queryset.filter(player__owner__username=self.kwargs.get('username'))


class LicenseDetailView(OwnerOrStaffMixin, DetailView):
    """Detail of a license."""

    template_name = "sports_manager/license/detail.html"
    model = License


class LicenseCreateView(CreateView):
    """Create a license for a logged user."""

    template_name = "sports_manager/license/create_form.html"
    # model = License
    form_class = LicenseCreationForm2

    def get_initial(self):
        initial = super().get_initial()
        initial['player'] = Player.objects.filter(owner__username=self.kwargs.get('username'))
        initial['category'] = Category.objects.none()
        initial['teams'] = Team.objects.none()
        print(initial)
        return initial

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s created successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.is_payed = False
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class LicenseCreateView2(FormView):
    """Create a license for a logged user."""

    template_name = "sports_manager/license/create_form.html"
    form_class = LicenseCreationForm2

    def get_initial(self):
        initial = super().get_initial()
        initial['player'] = Player.objects.filter(owner__username=self.kwargs.get('username'))
        initial['category'] = Category.objects.none()
        initial['teams'] = Team.objects.none()
        logger.debug(initial)
        return initial

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s created successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.is_payed = False
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class LicenseUpdateView(UpdateView):
    """Update a license for a logged user."""

    template_name = "sports_manager/license/update_form.html"
    model = License
    form_class = LicenseCreationForm

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s updated successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class LicenseDeleteView(DeleteView):
    """Delete a player's license."""

    template_name = "sports_manager/license/confirm_delete.html"
    model = License

    def get_queryset(self):
        """Return the list of license owned by the 'username'."""
        return super().get_queryset.filter(player__owner__username=self.kwargs.get('username'))

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("License for '%(name)s updated successfully") % {'name': self.object.player}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Validate the form."""
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        # Return directly the Http page because we are saving a m2m
        return HttpResponseRedirect(self.get_success_url())


class GetCategoryFromPlayerBirthday(View):

    http_method_names = ['get']

    def calculate_age_player(self, birthday):
        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    
    def get_list_of_category(self, age):
        qs = Category.objects.all()
        logger.debug(qs)

        qs = qs.exclude(max_age__lte=age)
        logger.debug(qs)

        return qs

    def get(self, request, *args, **kwargs):
        player_id = request.GET.get('player')
        player = Player.objects.get(id=player_id)
        player_age = self.calculate_age_player(player.birthday)

        logger.debug("{} {} age: {}".format(player.first_name, player.last_name, player_age))

        for category in Category.objects.all():
            logger.debug("{}, {}, {}".format(category.slug, category.min_age, category.max_age))
        
        self.get_list_of_category(player_age)

        d = {
            'player_age': player_age,
            'categories': [category.slug for category in self.get_list_of_category(player_age)]
        }
        return JsonResponse(d, safe=False)

