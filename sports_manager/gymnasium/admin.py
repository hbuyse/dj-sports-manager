# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.gymnasium.models import Gymnasium


@admin.register(Gymnasium)
class GymnasiumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'zip_code',
    )
