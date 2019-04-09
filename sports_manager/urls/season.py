# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.views import season as views

season_urlpatterns = [
    path("season/",
         view=views.SeasonListView.as_view(),
         name='season-list',
         ),
    path("season/create/",
         view=views.SeasonCreateView.as_view(),
         name='season-create',
         ),
    path("season/<slug:slug>/",
         view=views.SeasonDetailView.as_view(),
         name='season-detail',
         ),
    path("season/<slug:slug>/update/",
         view=views.SeasonUpdateView.as_view(),
         name='season-update',
         ),
    path("season/<slug:slug>/delete/",
         view=views.SeasonDeleteView.as_view(),
         name='season-delete',
         ),
]
