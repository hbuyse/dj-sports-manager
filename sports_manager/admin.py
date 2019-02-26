# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
import sports_manager
# from sports.models import Category, License, Player, Team, TimeSlot


@admin.register(sports_manager.models.category.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'min_age',
        'max_age'
    )


@admin.register(sports_manager.models.gymnasium.Gymnasium)
class GymnasiumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'zip_code',
    )

@admin.register(sports_manager.models.team.Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'category',
        'level',
        'sex'
    )

@admin.register(sports_manager.models.team.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        'team',
        'type',
        'day'
    )

@admin.register(sports_manager.models.player.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'owner',
    )

@admin.register(sports_manager.models.player.MedicalCertificate)
class MedicalCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'player_first_name',
        'player_last_name',
        'start',
        'validation'
    )

    def player_first_name(self, obj):
        return obj.player.first_name

    def player_last_name(self, obj):
        return obj.player.last_name

@admin.register(sports_manager.models.player.EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = (
        'player_first_name',
        'player_last_name',
        'phone',
    )

    def player_first_name(self, obj):
        return obj.player.first_name

    def player_last_name(self, obj):
        return obj.player.last_name

@admin.register(sports_manager.models.license.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'season',
        'number',
        'is_payed',
    )

    def season(self, obj):
        return obj.get_season()
