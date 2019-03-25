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
         view=views.PlayerCreateView.as_view(),
         name='player-create',
         ),
    path("<str:username>/player/<str:slug>/",
         view=views.PlayerDetailView.as_view(),
         name='player-detail',
         ),
    path("<str:username>/player/<str:slug>/update/",
         view=views.PlayerUpdateView.as_view(),
         name='player-update',
         ),
    path("<str:username>/player/<str:slug>/delete/",
         view=views.PlayerDeleteView.as_view(),
         name='player-delete',
         )
]

# player_urlpatterns += [
#     path("<str:username>/player/<str:slug>/emergency-contact/",
#          view=views.EmergencyContactListView.as_view(),
#          name='player-emergency-contact-list',
#          ),
#     path("<str:username>/player/<str:slug>/emergency-contact/create/",
#          view=views.EmergencyContactDetailView.as_view(),
#          name='player-emergency-contact-detail',
#          ),
#     path("<str:username>/player/<str:slug>/emergency-contact/<int:pk>/",
#          view=views.EmergencyContactCreateView.as_view(),
#          name='player-emergency-contact-create',
#          ),
#     path("<str:username>/player/<str:slug>/emergency-contact/<int:pk>/update/",
#          view=views.EmergencyContactUpdateView.as_view(),
#          name='player-emergency-contact-update',
#          ),
#     path("<str:username>/player/<str:slug>/emergency-contact/<int:pk>/delete/",
#          view=views.EmergencyContactDeleteView.as_view(),
#          name='player-emergency-contact-delete',
#          )
# ]

# player_urlpatterns += [
#     path("<str:username>/player/<str:slug>/medical-certificate/",
#          view=views.MedicalCertificateListView.as_view(),
#          name='player-medical-certificate-list',
#          ),
#     path("<str:username>/player/<str:slug>/medical-certificate/create/",
#          view=views.MedicalCertificateDetailView.as_view(),
#          name='player-medical-certificate-detail',
#          ),
#     path("<str:username>/player/<str:slug>/medical-certificate/<int:pk>/",
#          view=views.MedicalCertificateCreateView.as_view(),
#          name='player-medical-certificate-create',
#          ),
#     path("<str:username>/player/<str:slug>/medical-certificate/<int:pk>/update/",
#          view=views.MedicalCertificateUpdateView.as_view(),
#          name='player-medical-certificate-update',
#          ),
#     path("<str:username>/player/<str:slug>/medical-certificate/<int:pk>/delete/",
#          view=views.MedicalCertificateDeleteView.as_view(),
#          name='player-medical-certificate-delete',
#          )
# ]