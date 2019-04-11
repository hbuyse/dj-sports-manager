# -*- coding: utf-8 -*-
"""Urls."""

# Current django project
from sports_manager.urls.category import category_urlpatterns
from sports_manager.urls.gymnasium import gymnasium_urlpatterns
from sports_manager.urls.license import license_urlpatterns
from sports_manager.urls.player import player_urlpatterns
from sports_manager.urls.staff import staff_urlpatterns
from sports_manager.urls.team import team_urlpatterns

app_name = 'sports-manager'
urlpatterns = list()
urlpatterns += category_urlpatterns
urlpatterns += gymnasium_urlpatterns
urlpatterns += license_urlpatterns
urlpatterns += player_urlpatterns
urlpatterns += staff_urlpatterns
urlpatterns += team_urlpatterns