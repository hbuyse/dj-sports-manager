# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.player import views

player_urlpatterns = [
    path("<str:username>/player/",
         view=views.PlayerListView.as_view(),
         name='player-list',
         ),
    path("<str:username>/player/create/",
         view=views.create_new_player,
         name='player-create',
         ),
    path("<str:username>/player/<int:pk>/",
         view=views.PlayerDetailView.as_view(),
         name='player-detail',
         ),
    path("<str:username>/player/<int:pk>/update/",
         view=views.PlayerUpdateView.as_view(),
         name='player-update',
         ),
    path("<str:username>/player/<int:pk>/delete/",
         view=views.PlayerDeleteView.as_view(),
         name='player-delete',
         ),
]
