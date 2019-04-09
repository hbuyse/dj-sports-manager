# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.views import license as views

license_urlpatterns = [
    path("<str:username>/license/",
         view=views.LicenseListView.as_view(),
         name='license-list',
         ),
    path("<str:username>/license/create/",
         view=views.LicenseCreateView.as_view(),
         name='license-create',
         ),
    path("<str:username>/license/<int:pk>/",
         view=views.LicenseDetailView.as_view(),
         name='license-detail',
         ),
    path("<str:username>/license/<int:pk>/update/",
         view=views.LicenseUpdateView.as_view(),
         name='license-update',
         ),
    path("<str:username>/license/<int:pk>/delete/",
         view=views.LicenseDeleteView.as_view(),
         name='license-delete',
         ),
]
