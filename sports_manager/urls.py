# -*- coding: utf-8 -*-
"""Urls."""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Current django project
import sports_manager.views.category as vcategory
import sports_manager.views.gymnasium as vgymnasium
import sports_manager.views.license as vlicense
import sports_manager.views.player as vplayer
import sports_manager.views.team as vteam
import sports_manager.views.timeslot as vtimeslot
from sports_manager import views

app_name = 'sports-manager'
urlpatterns = [
     path("category/",
          view=vcategory.CategoryListView.as_view(),
          name='category-list',
          ),
     path("category/create/",
          view=vcategory.CategoryCreateView.as_view(),
          name='category-create',
          ),
     path("category/<str:slug>/",
          view=vcategory.CategoryDetailView.as_view(),
          name='category-detail',
          ),
     path("category/<str:slug>/update/",
          view=vcategory.CategoryUpdateView.as_view(),
          name='category-update',
          ),
     path("category/<str:slug>/delete/",
          view=vcategory.CategoryDeleteView.as_view(),
          name='category-delete',
          )
]

urlpatterns += [
     path("team/",
          view=vteam.TeamListView.as_view(),
          name='team-list',
          ),
     path("team/create/",
          view=vteam.TeamCreateView.as_view(),
          name='team-create',
          ),
     path("team/<str:slug>/",
          view=vteam.TeamDetailView.as_view(),
          name='team-detail',
          ),
     path("team/<str:slug>/update/",
          view=vteam.TeamUpdateView.as_view(),
          name='team-update',
          ),
     path("team/<str:slug>/delete/",
          view=vteam.TeamDeleteView.as_view(),
          name='team-delete',
          ),
     path("team/<str:slug>/time-slot/",
          view=vtimeslot.TeamTimeSlotListView.as_view(),
          name='team-time-slot-list',
          ),
     path("team/<str:slug>/time-slot/create/",
          view=vtimeslot.TeamTimeSlotCreateView.as_view(),
          name='team-time-slot-create',
          ),
     path("team/<str:slug>/time-slot/<int:pk>/update/",
          view=vtimeslot.TeamTimeSlotUpdateView.as_view(),
          name='team-time-slot-update',
          ),
     path("team/<str:slug>/time-slot/<int:pk>/delete/",
          view=vtimeslot.TeamTimeSlotDeleteView.as_view(),
          name='team-time-slot-delete',
          )
]

urlpatterns += [
     path("<str:username>/license/",
          view=vlicense.LicenseListView.as_view(),
          name='license-list',
          ),
     path("<str:username>/license/create/",
          view=vlicense.LicenseCreateView.as_view(),
          name='license-create',
          ),
     path("<str:username>/license/<int:pk>/",
          view=vlicense.LicenseDetailView.as_view(),
          name='license-detail',
          ),

     path("<str:username>/player/",
          view=vplayer.PlayerListView.as_view(),
          name='player-list',
          ),
     path("<str:username>/player/create/",
          view=vplayer.create_new_player,
          name='player-create',
          ),
]

urlpatterns += [
     path("gymnasium/",
          view=vgymnasium.GymnasiumListView.as_view(),
          name='gymnasium-list',
          ),
     path("gymnasium/create/",
          view=vgymnasium.GymnasiumCreateView.as_view(),
          name='gymnasium-create',
          ),
     path("gymnasium/<slug:slug>/",
          view=vgymnasium.GymnasiumDetailView.as_view(),
          name='gymnasium-detail',
          ),
     path("gymnasium/<slug:slug>/update/",
          view=vgymnasium.GymnasiumUpdateView.as_view(),
          name='gymnasium-update',
          ),
     path("gymnasium/<slug:slug>/delete/",
          view=vgymnasium.GymnasiumDeleteView.as_view(),
          name='gymnasium-delete',
          )
]
