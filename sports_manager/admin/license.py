# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.models.license import License


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    """License admin object."""

    list_display = (
        'player',
        'season',
        'number',
        'is_payed',
    )

    def season(self, obj):
        """Return the license season."""
        return obj.season
