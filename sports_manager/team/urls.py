# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.team import views

team_urlpatterns = [
    path("team/",
         view=views.TeamListView.as_view(),
         name='team-list',
         ),
    path("team/create/",
         view=views.TeamCreateView.as_view(),
         name='team-create',
         ),
    path("team/<str:slug>/",
         view=views.TeamDetailView.as_view(),
         name='team-detail',
         ),
    path("team/<str:slug>/update/",
         view=views.TeamUpdateView.as_view(),
         name='team-update',
         ),
    path("team/<str:slug>/delete/",
         view=views.TeamDeleteView.as_view(),
         name='team-delete',
         ),
    path("team/<str:slug>/time-slot/",
         view=views.TeamTimeSlotListView.as_view(),
         name='team-time-slot-list',
         ),
    path("team/<str:slug>/time-slot/create/",
         view=views.TeamTimeSlotCreateView.as_view(),
         name='team-time-slot-create',
         ),
    path("team/<str:slug>/time-slot/<int:pk>/update/",
         view=views.TeamTimeSlotUpdateView.as_view(),
         name='team-time-slot-update',
         ),
    path("team/<str:slug>/time-slot/<int:pk>/delete/",
         view=views.TeamTimeSlotDeleteView.as_view(),
         name='team-time-slot-delete',
         )
]