# coding=utf-8

"""Admin."""

# Django
from django.contrib import admin

# Current django project
from sports_manager.player.models import EmergencyContact, MedicalCertificate, Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Player admin object."""

    list_display = (
        'first_name',
        'last_name',
        'owner',
    )


@admin.register(MedicalCertificate)
class MedicalCertificateAdmin(admin.ModelAdmin):
    """Medical certificate admin object."""

    list_display = (
        'player_first_name',
        'player_last_name',
        'start',
        'validation'
    )

    def player_first_name(self, obj):
        """Return the player's first name linked to the medical certificate.

        This method is used to sort the medical certificates by the first name of the linked player.
        """
        return obj.player.first_name

    def player_last_name(self, obj):
        """Return the player's last name linked to the medical certificate.

        This method is used to sort the medical certificates by the last name of the linked player.
        """
        return obj.player.last_name


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Emergency admin object."""

    list_display = (
        'player_first_name',
        'player_last_name',
        'phone',
    )

    def player_first_name(self, obj):
        """Return the player's first name linked to the emergency contact.

        This method is used to sort the emergency contacts by the first name of the linked player.
        """
        return obj.player.first_name

    def player_last_name(self, obj):
        """Return the player's last name linked to the emergency contacts.

        This method is used to sort the emergency contactss by the last name of the linked player.
        """
        return obj.player.last_name
