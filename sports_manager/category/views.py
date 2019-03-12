# -*- coding: utf-8 -*-
"""Category model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.category.models import Category
from sports_manager.mixins import StaffMixin

logger = logging.getLogger(__name__)


class CategoryListView(ListView):
    """View that returns the list of categories."""

    model = Category
    template_name = "sports_manager/category/list.html"


class CategoryDetailView(DetailView):
    """View that returns the details of a category."""

    model = Category
    slug_field = 'slug'
    template_name = "sports_manager/category/detail.html"


class CategoryCreateView(LoginRequiredMixin, StaffMixin, CreateView):
    """View that creates a new category."""

    template_name = "sports_manager/category/create_form.html"
    model = Category
    fields = [
        'name',
        'min_age',
        'max_age',
        'summary',
        'description',
        'img',
    ]

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Category '%(name)s' added successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class CategoryUpdateView(LoginRequiredMixin, StaffMixin, UpdateView):
    """View that updates a new category."""

    template_name = "sports_manager/category/update_form.html"
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

    def get_success_url(self):
        """Get the URL after the success."""
        msg = _("Category '%(name)s' updated successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return self.object.get_absolute_url()


class CategoryDeleteView(LoginRequiredMixin, StaffMixin, DeleteView):
    """View that deletes a new category."""

    template_name = "sports_manager/category/confirm_delete.html"
    model = Category
    slug_field = 'slug'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        msg = _("Category '%(name)s' deleted successfully") % {'name': self.object.name}
        messages.success(self.request, msg)
        return reverse('sports-manager:category-list')
