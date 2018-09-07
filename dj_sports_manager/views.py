# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Category,
	Team,
	Practice,
	License,
)


class CategoryCreateView(CreateView):

    model = Category


class CategoryDeleteView(DeleteView):

    model = Category


class CategoryDetailView(DetailView):

    model = Category


class CategoryUpdateView(UpdateView):

    model = Category


class CategoryListView(ListView):

    model = Category


class TeamCreateView(CreateView):

    model = Team


class TeamDeleteView(DeleteView):

    model = Team


class TeamDetailView(DetailView):

    model = Team


class TeamUpdateView(UpdateView):

    model = Team


class TeamListView(ListView):

    model = Team


class PracticeCreateView(CreateView):

    model = Practice


class PracticeDeleteView(DeleteView):

    model = Practice


class PracticeDetailView(DetailView):

    model = Practice


class PracticeUpdateView(UpdateView):

    model = Practice


class PracticeListView(ListView):

    model = Practice


class LicenseCreateView(CreateView):

    model = License


class LicenseDeleteView(DeleteView):

    model = License


class LicenseDetailView(DetailView):

    model = License


class LicenseUpdateView(UpdateView):

    model = License


class LicenseListView(ListView):

    model = License

