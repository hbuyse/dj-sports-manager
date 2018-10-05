# -*- coding: utf-8 -*-
"""Views."""

from .views_category import (
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
)

from .views_team import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)

from .views_timeslot import (
    TeamTimeSlotListView,
    TeamTimeSlotDetailView,
    TeamTimeSlotCreateView,
    TeamTimeSlotUpdateView,
    TeamTimeSlotDeleteView
)

from .views_license import (
    LicenseListView,
    LicenseDetailView,
    LicenseCreateView
)
