# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
import sports_manager
from sports.models import Category, License, Player, Team, TimeSlot


@admin.register(sports_manager.category.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'min_age',
        'max_age'
    )

@admin.register(sports_manager.team.Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'category',
        'level',
        'sex'
    )

@admin.register(sports_manager.team.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'type_time_slot',
        'day'
    )

@admin.register(sports_manager.player.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'owner',
    )

@admin.register(sports_manager.license.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'license_number',
        'is_payed',
    )
