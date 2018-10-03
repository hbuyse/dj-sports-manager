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
        messages.success(self.request, "Category '{}' updated successfully".format(self.object.name))
        return reverse('dj-sports-manager:category-detail', kwargs={'slug': self.object.slug})


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
        return reverse('dj-sports-manager:categories-list')
