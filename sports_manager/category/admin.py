# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category administration."""

    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'min_age',
        'max_age'
    )
