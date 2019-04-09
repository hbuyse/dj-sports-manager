# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.models.season import Season


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """Season admin object."""

    list_display = (
        'start',
        'end',
    )
