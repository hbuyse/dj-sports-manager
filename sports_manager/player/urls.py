# -*- coding: utf-8 -*-
"""Urls."""

# Standard library
import logging

# Django
from django.conf import settings
from django.urls import path

# Current django project
from sports_manager.player import views

logger = logging.getLogger(__name__)

player_urlpatterns = [
    path("<str:username>/player/",
         view=views.PlayerListView.as_view(),
         name='player-list'
         ),
]

if hasattr(settings, 'SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE') and settings.SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE:
    player_urlpatterns += [
        path("<str:username>/player/create/",
             view=views.PlayerAllInOneCreateView.as_view(),
             name='player-create'
             )
    ]
else:
    player_urlpatterns += [
        path("<str:username>/player/create/",
             view=views.PlayerCreateView.as_view(),
             name='player-create'
             )
    ]

player_urlpatterns += [
    path("<str:username>/player/<str:slug>/",
         view=views.PlayerDetailView.as_view(),
         name='player-detail'
         ),
    path("<str:username>/player/<str:slug>/delete/",
         view=views.PlayerDeleteView.as_view(),
         name='player-delete'
         )
]

if hasattr(settings, 'SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE') and settings.SPORTS_MANAGER_PLAYER_FORM_ALL_IN_ONE:
    player_urlpatterns += [
        path("<str:username>/player/<str:slug>/update/",
             view=views.PlayerAllInOneUpdateView.as_view(),
             name='player-update'
             )
    ]
else:
    player_urlpatterns += [
        path("<str:username>/player/<str:slug>/update/",
             view=views.PlayerUpdateView.as_view(),
             name='player-update'
             )
    ]



player_urlpatterns += [
    path("<str:username>/player/<str:player>/emergency-contact/",
         view=views.EmergencyContactListView.as_view(),
         name='player-emergency-contact-list'
         ),
    path("<str:username>/player/<str:player>/emergency-contact/create/",
         view=views.EmergencyContactDetailView.as_view(),
         name='player-emergency-contact-create'
         ),
    path("<str:username>/player/<str:player>/emergency-contact/<int:pk>/",
         view=views.EmergencyContactCreateView.as_view(),
         name='player-emergency-contact-detail'
         ),
    path("<str:username>/player/<str:player>/emergency-contact/<int:pk>/update/",
         view=views.EmergencyContactUpdateView.as_view(),
         name='player-emergency-contact-update'
         ),
    path("<str:username>/player/<str:player>/emergency-contact/<int:pk>/delete/",
         view=views.EmergencyContactDeleteView.as_view(),
         name='player-emergency-contact-delete'
         ),
]

player_urlpatterns += [
    path("<str:username>/player/<str:player>/medical-certificate/",
         view=views.MedicalCertificateListView.as_view(),
         name='player-medical-certificate-list',
         ),
    path("<str:username>/player/<str:player>/medical-certificate/create/",
         view=views.MedicalCertificateCreateView.as_view(),
         name='player-medical-certificate-create',
         ),
    path("<str:username>/player/<str:player>/medical-certificate/<int:pk>/",
         view=views.MedicalCertificateDetailView.as_view(),
         name='player-medical-certificate-detail',
         ),
    path("<str:username>/player/<str:player>/medical-certificate/<int:pk>/update/",
         view=views.MedicalCertificateUpdateView.as_view(),
         name='player-medical-certificate-update',
         ),
    path("<str:username>/player/<str:player>/medical-certificate/<int:pk>/delete/",
         view=views.MedicalCertificateDeleteView.as_view(),
         name='player-medical-certificate-delete',
         ),
]

if hasattr(settings, 'SPORTS_MANAGER_MEDICAL_CERTIFICATE_MAX_RENEW'):
    player_urlpatterns += [
        path("<str:username>/player/<str:player>/medical-certificate/<int:pk>/renew/",
             view=views.MedicalCertificateRenewView.as_view(),
             name='player-medical-certificate-renew'
             )
    ]
