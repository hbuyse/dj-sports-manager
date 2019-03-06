# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'owner',
    )

@admin.register(MedicalCertificate)
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

@admin.register(EmergencyContact)
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
