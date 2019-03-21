# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.license import views

license_urlpatterns = [
    path("<str:username>/license/",
         view=views.LicenseListView.as_view(),
         name='license-list',
         ),
    path("<str:username>/license/create/",
         view=views.LicenseCreateView2.as_view(),
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
    path("get_list_categories/",
         view=views.LicenseCreateAjaxGetCategories.as_view(),
         name='license-get-list-categories'
         ),
    path("get_list_teams/",
         view=views.LicenseCreateAjaxGetTeams.as_view(),
         name='license-get-list-teams'
         ),
]
