# -*- coding: utf-8 -*-
"""Category urls."""

# Django
from django.urls import path

# Current django project
from sports_manager.views import category as views

category_urlpatterns = [
    path("category/",
         view=views.CategoryListView.as_view(),
         name='category-list',
         ),
    path("category/create/",
         view=views.CategoryCreateView.as_view(),
         name='category-create',
         ),
    path("category/<str:slug>/",
         view=views.CategoryDetailView.as_view(),
         name='category-detail',
         ),
    path("category/<str:slug>/update/",
         view=views.CategoryUpdateView.as_view(),
         name='category-update',
         ),
    path("category/<str:slug>/delete/",
         view=views.CategoryDeleteView.as_view(),
         name='category-delete',
         )
]
