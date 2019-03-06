# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.license.models import License


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'season',
        'number',
        'is_payed',
    )

    def season(self, obj):
        return obj.get_season()
