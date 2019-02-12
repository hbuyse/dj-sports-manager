# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, unicode_literals

# Django
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('', include('sports_manager.urls', namespace='sports_manager')),
]
