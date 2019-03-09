# -*- coding: utf-8 -*-
"""Urls."""

# Current django project
from sports_manager.category.urls import category_urlpatterns
from sports_manager.gymnasium.urls import gymnasium_urlpatterns
from sports_manager.license.urls import license_urlpatterns
from sports_manager.player.urls import player_urlpatterns
from sports_manager.team.urls import team_urlpatterns

app_name = 'sports-manager'
urlpatterns = list()
urlpatterns += category_urlpatterns
urlpatterns += gymnasium_urlpatterns
urlpatterns += license_urlpatterns
urlpatterns += player_urlpatterns
urlpatterns += team_urlpatterns
