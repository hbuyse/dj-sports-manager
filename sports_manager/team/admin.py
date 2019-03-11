# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.team.models import Team, TimeSlot


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Team admin."""

    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'category',
        'level',
        'sex'
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Time slot admin."""

    list_display = (
        'team',
        'type',
        'day'
    )
