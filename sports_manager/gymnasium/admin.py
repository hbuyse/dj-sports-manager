# coding=utf-8

"""Gymansium admin models."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.gymnasium.models import Gymnasium


@admin.register(Gymnasium)
class GymnasiumAdmin(admin.ModelAdmin):
    """Gymnasium admin object."""

    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'zip_code',
    )
