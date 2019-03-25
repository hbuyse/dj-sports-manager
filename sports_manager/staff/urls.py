# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path
from django.views.generic import TemplateView

# Current django project
from sports_manager.staff import views

staff_urlpatterns = [
    path("staff/",
         view=views.StaffLinksView.as_view(),
         name='staff-index',
         ),
    path("staff/licenses/",
         view=views.StaffLicenseListView.as_view(),
         name='staff-licenses-list',
         ),
]