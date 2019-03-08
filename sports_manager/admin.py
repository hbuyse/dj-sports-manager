# coding=utf-8

"""Admin."""

# Current django project
from sports_manager.category.admin import CategoryAdmin  # noqa
from sports_manager.gymnasium.admin import GymnasiumAdmin  # noqa
from sports_manager.license.admin import LicenseAdmin  # noqa
from sports_manager.player.admin import EmergencyContactAdmin, MedicalCertificateAdmin, PlayerAdmin  # noqa
from sports_manager.team.admin import TeamAdmin, TimeSlotAdmin  # noqa
