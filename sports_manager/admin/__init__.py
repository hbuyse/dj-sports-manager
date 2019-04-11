# coding=utf-8

"""Admin."""

# Current django project
from sports_manager.admin.category import CategoryAdmin  # noqa
from sports_manager.admin.gymnasium import GymnasiumAdmin  # noqa
from sports_manager.admin.license import LicenseAdmin  # noqa
from sports_manager.admin.player import EmergencyContactAdmin, MedicalCertificateAdmin, PlayerAdmin  # noqa
from sports_manager.admin.team import TeamAdmin, TimeSlotAdmin  # noqa

__all__ = (CategoryAdmin, GymnasiumAdmin, LicenseAdmin, EmergencyContactAdmin, MedicalCertificateAdmin, PlayerAdmin,
           TeamAdmin, TimeSlotAdmin)