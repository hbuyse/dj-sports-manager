# -*- coding: utf-8 -*-
"""Gymnasium urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.gymnasium import views

gymnasium_urlpatterns = [
    path("gymnasium/",
         view=views.GymnasiumListView.as_view(),
         name='gymnasium-list',
         ),
    path("gymnasium/create/",
         view=views.GymnasiumCreateView.as_view(),
         name='gymnasium-create',
         ),
    path("gymnasium/<slug:slug>/",
         view=views.GymnasiumDetailView.as_view(),
         name='gymnasium-detail',
         ),
    path("gymnasium/<slug:slug>/update/",
         view=views.GymnasiumUpdateView.as_view(),
         name='gymnasium-update',
         ),
    path("gymnasium/<slug:slug>/delete/",
         view=views.GymnasiumDeleteView.as_view(),
         name='gymnasium-delete',
         )
]
