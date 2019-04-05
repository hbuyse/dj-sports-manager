# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.urls import path

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
    path("staff/email/",
         view=views.StaffSendEmailView.as_view(),
         name='staff-send-email',
         ),
]
