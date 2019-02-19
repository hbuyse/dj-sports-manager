# -*- coding: utf-8 -*-
"""Category model views."""

# Standard library
import logging

# Django
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Current django project
from sports_manager.models import Category

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
        messages.success(self.request, "Category '{}' added successfully".format(self.object.name))
        return self.object.get_absolute_url()


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
        messages.success(self.request, "Category '{}' updated successfully".format(self.object.name))
        return self.object.get_absolute_url()


class CategoryDeleteView(DeleteView):
    """View that deletes a new category."""

    model = Category
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
        messages.success(self.request, "Category '{}' deleted successfully".format(self.object.name))
        return reverse('sports-manager:category-list')
